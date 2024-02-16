import bentoml
import numpy as np
from bentoml.io import NumpyNdarray
my_best_model = bentoml.models.get('my_best_model:latest')
my_best_model_runner = my_best_model.to_runner()


svc = bentoml.Service('my_model', runners=[my_best_model_runner])

@svc.api(input=NumpyNdarray(),output=NumpyNdarray())
def predict(input_arr:np.ndarray):
    return my_best_model_runner.predict.run(input_arr)


