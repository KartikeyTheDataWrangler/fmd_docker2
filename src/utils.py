import os,sys
sys.path.append(os.getcwd())
import dill
from prefect import task, flow


@task
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    
    except Exception as e:
        raise e

   
@task
def read_object(file_path):
    try:
        with open(file_path, "rb") as obj:
            return dill.load(obj)
    except Exception as e:
        raise e
    
    
