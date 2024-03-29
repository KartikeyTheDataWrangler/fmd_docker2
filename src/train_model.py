import pandas as pd
import numpy as np
import os,sys
from utils import save_object,read_object
from prefect import flow,task
from transform import transform_df
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,  roc_auc_score
import mlflow
import bentoml
import subprocess
from prefect.task_runners import SequentialTaskRunner
from bentoml.io import NumpyNdarray
from fetch_data import fetch
import os, shutil
from dotenv import load_dotenv


@task(name="delete model directories")
def delete_model_directries():
    path_='artifacts\current_best_model'
    if os.path.exists(path=path_):
        shutil.rmtree(path_)
        
    path_2 = 'dvcremote\current_best_model'
    if os.path.exists(path=path_2):
        shutil.rmtree(path_2)

    path_3 = 'artifacts\overall_best_model'
    if os.path.exists(path=path_3):
        shutil.rmtree(path_3)
   


@task
def read_csv():
    df_=pd.read_csv('artifacts\creditcard.csv')
    return df_
@task(name="split_into_train_test")
def split_data(df):
    train, test = train_test_split(df,test_size=0.2)
    
    return train, test


@task(name="train_tune_model")
def grid_search(transformed_df_train):
    param_rf = {
    'n_estimators': [25,50],
        'max_depth': [4, 6,8,],
    'min_samples_leaf': [ 10,12,15],
        'criterion' :['gini', 'entropy'],
        }
    
    X_train = transformed_df_train.drop('default.payment.next.month',axis=1)
    y_train = transformed_df_train['default.payment.next.month']
    
        
    grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_rf, cv=2, n_jobs=-1)
    grid_search.fit(X_train,y_train)
    best_rf_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    return best_model, best_rf_params


@task(name="logging_model_mlflow_bentoml")
def log_model(train_df,test_df,best_params,best_model):
    
    
    load_dotenv(".env")
    DAGSHUB_USER = os.getenv('MLFLOW_TRACKING_USERNAME')
    DAGSHUB_TOKEN = os.getenv('MLFLOW_TRACKING_PASSWORD')
    
    
    os.environ["MLFLOW_TRACKING_USERNAME"] = DAGSHUB_USER
    os.environ["MLFLOW_TRACKING_PASSWORD"] = DAGSHUB_TOKEN
    #print(DAGSHUB_USER, DAGSHUB_TOKEN)
    
    dagshub_url = "https://dagshub.com/KartikeyTheDataWrangler/fmd_docker2.mlflow"
    
    mlflow.set_tracking_uri(dagshub_url)
    X_train = train_df.drop('default.payment.next.month',axis=1)
    y_train = train_df['default.payment.next.month']
    X_test = test_df.drop('default.payment.next.month',axis=1)
    y_test = test_df['default.payment.next.month']
    
    exp = mlflow.set_experiment(experiment_name='credit_card_trials')
    experimentid = mlflow.get_experiment_by_name('credit_card_trials').experiment_id
    print(experimentid)
    
    with mlflow.start_run():
        mlflow.log_params(best_params)
        best_model.fit(X_train,y_train)
        predictions = best_model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        mlflow.log_metric('accuracy', accuracy)

        auc = roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
        mlflow.log_metric('auc', auc)
        
        mlflow.sklearn.log_model(best_model, "best model")
        
        
        mlflow.sklearn.save_model(sk_model= best_model, path= 'artifacts/current_best_model')
        mlflow.sklearn.save_model(sk_model = best_model, path= 'dvcremote/current_best_model')
    
        
        
        
        bentoml.sklearn.save_model( name="sklearn_best",model=best_model)
        
        #bentoml.models.export_model('sklearn_best:latest', 'artifacts/sklerarn_best_')
        
        df = mlflow.search_runs(experiment_ids=[exp.experiment_id])
        #df.to_csv('sdfsdf.csv')
        print(df['run_id'][0])
        return df

@task
def add_to_bento(mlflow_df):
    best_run = mlflow_df.iloc[mlflow_df['metrics.accuracy'].idxmax()]
    best_model_run = best_run['run_id']
    model_uri = f"runs:/{best_model_run}/best model"
    print(model_uri)
    best_model_overall = mlflow.sklearn.load_model(model_uri)
    print(best_model_overall)
    mlflow.sklearn.save_model(sk_model = best_model_overall, path= 'artifacts/overall_best_model')
    
    
    
    bento_model = bentoml.mlflow.import_model("my_best_model", model_uri)
    #bentoml.models.export_model('my_best_model:latest', 'artifacts/my_best_model_')
    
    print("\n Model imported to BentoML: %s" % bento_model)
    return best_model_overall

#bentoml.mlflow.load_model()
    




@flow(name="train_flow", task_runner=SequentialTaskRunner())
def basic_transformationi():
    fetch()
    delete_model_directries()
    df_ = read_csv()
    df = transform_df(df=df_)
    print(df)
    save_object(file_path=r'artifacts\transformer_pic', obj=transform_df)
    train, test = split_data(df)
    bestmodel, bestparams = grid_search(transformed_df_train=train)
    print(bestparams)
    #save_object(file_path=r'artifacts\best_model', obj=bestmodel)
    #save_object(file_path=r'dvcremote\best_model', obj=bestmodel)
    run_df = log_model(train_df=train,test_df=test,best_params=bestparams,best_model=bestmodel)  
    best_model_ovrl= add_to_bento(mlflow_df=run_df)

       
if __name__ =='__main__':
    basic_transformationi()
    #os.chdir("src")
    #subprocess.run(["bentoml" ,"serve" ,"service:svc"])
    
    
    
    
    


    




    
    