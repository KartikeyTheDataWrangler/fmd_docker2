import bentoml

from bentoml.io import NumpyNdarray
my_best_model = bentoml.models.import_model('artifacts\my_best_model.bentomodel')
my_best_model_runner = my_best_model.to_runner()


svc = bentoml.Service('my_model', runners=[my_best_model_runner])

@svc.api(input=bentoml.io.NumpyNdarray(),output=bentoml.io.NumpyNdarray(),route='/beleth')
def predict(input_arr):
    return my_best_model_runner.predict.run(input_arr)