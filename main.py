
import os,sys
sys.path.append(os.getcwd()+"/src")
from src.utils import read_object
from src.fetch_data import fetch
from prefect import flow,task

from src.train_model import read_csv
import pandas as pd
from prefect.task_runners import SequentialTaskRunner

import subprocess



@task(log_prints=True,name='print hello')
def prnt():
    print(" Insta kam kar Bhaiii")
    

@flow(log_prints=True,name='main_flow',task_runner=SequentialTaskRunner())
def someting():
    prnt()
    fetch()
    df_=read_csv()
    tr = read_object(file_path=r"artifacts\transformer_pic")
    
    df = tr(df_)
    print(df)
    

   

    
someting()
