
import os,sys
sys.path.append(os.getcwd()+"/src")
from src.utils import read_object
from src.fetch_data import fetch
from prefect import flow
import pickle
import numpy as np

with open(file='artifacts\current_best_model\model.pkl', mode="rb") as file:
    current_model = pickle.load(file)


prediction = current_model.predict(np.array([55,2000,2,2,2,57,0,1284,833]).reshape(1,-1))

print(prediction)



    

