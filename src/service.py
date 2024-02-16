import bentoml
import numpy as np
from bentoml.io import NumpyNdarray

my_best_model = bentoml.models.get('my_best_model:latest')
my_best_model_runner = my_best_model.to_runner()

sklearn_best_model = bentoml.models.get('sklearn_best:latest')
sklearn_best_model_runner = sklearn_best_model.to_runner()

svc = bentoml.Service('my_model', runners=[my_best_model_runner,sklearn_best_model_runner])

@svc.api(input=NumpyNdarray(),output=NumpyNdarray())
def best_model_predict(input_arr:np.ndarray):
    return my_best_model_runner.predict.run(input_arr)

@svc.api(input=NumpyNdarray(),output=NumpyNdarray())
def sklerarn_predict(input_arr:np.ndarray):
    return sklearn_best_model_runner.predict.run(input_arr)

