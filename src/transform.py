import pandas as pd
from prefect import task,flow



@task
def transform_df(df):
    df['avg_pay'] = (df['PAY_0'] +df['PAY_2']+df['PAY_3']+df['PAY_4']+
                      df['PAY_5']+df['PAY_6'])//6
    df['avg_bill'] = (df['BILL_AMT1']+df['BILL_AMT2']+df['BILL_AMT3']+
                      df['BILL_AMT4']+df['BILL_AMT5']+df['BILL_AMT6'])//6
    
    df['avg_pay_amt'] = (df['PAY_AMT1']+df['PAY_AMT2']+df['PAY_AMT3']
                         +df['PAY_AMT4']+df['PAY_AMT5']+df['PAY_AMT6'])/6
    df_ = df.drop(['PAY_0',
       'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2',        
       'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
       'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'], axis=1)
    
    return df_



'''
df_ = pd.read_csv('artifacts/creditcard.csv')
df =transform_df(df=df_)
print(df)
'''