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
from bentoml.io import NumpyNdarray


@task(name="model tracking uri none")
def mlflow_tracking_none():
    mlflow.set_tracking_uri(None)


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
        'max_depth': [2, 4, 6,8,10 ],
    'min_samples_leaf': [ 6,8,10,12,15],
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
    mlflow.set_tracking_uri(None)
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
        
        bentoml.sklearn.save_model( name="sklearn_best",model=best_model)
        df = mlflow.search_runs(experiment_ids=[exp.experiment_id])
        #df.to_csv('sdfsdf.csv')
        return df
    
@task
def add_to_bento(mlflow_df):
    best_run = mlflow_df.iloc[mlflow_df['metrics.accuracy'].idxmax()]
    best_model_run = best_run['run_id']
    model_uri = f"runs:/{best_model_run}/best model"
    print(model_uri)
    bento_model = bentoml.mlflow.import_model("my_best_model", model_uri)
    
    print("\n Model imported to BentoML: %s" % bento_model)
    

#bentoml.mlflow.load_model()
    



if __name__ =='__main__':
    @flow(name="train_flow")
    def basic_transformationi():
       
        df_ = read_csv()
        df = transform_df(df=df_)
        print(df)
        save_object(file_path=r'artifacts\transformer_pic', obj=transform_df)
        train, test = split_data(df)
        bestmodel, bestparams = grid_search(transformed_df_train=train)
        print(bestparams)
        save_object(file_path=r'artifacts\besy_model', obj=bestmodel)
        run_df = log_model(train_df=train,test_df=test,best_params=bestparams,best_model=bestmodel)  
        add_to_bento(mlflow_df=run_df)
    
    basic_transformationi()
    
    
    
    
    
    


    




    
    