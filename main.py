
import os,sys
sys.path.append(os.getcwd()+"/src")
from src.utils import read_object
from src.fetch_data import fetch
from prefect import flow



@flow()
def read_obj():
    model = read_object(file_path= r"dvcremote\best_model_overall")
    prediction = model.predict()
    print(prediction)

read_object()

    

    

   

    

