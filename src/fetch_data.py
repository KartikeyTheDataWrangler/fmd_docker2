import requests
from prefect import task, flow

@task(retries=3, retry_delay_seconds=5)
def fetch_data(url: str, filepath: str):
    req = requests.get(url)
    csv_content = req.text
    with open(filepath, 'w') as file:
        file.write(csv_content)


@flow(flow_run_name="data fetch")
def fetch():
    
    fetch_data(url='https://raw.githubusercontent.com/KartikeyTheDataWrangler/fmd_docker2/main/UCI_Credit_Card.csv',
        filepath='artifacts/creditcard.csv  '
        )
    

    
    