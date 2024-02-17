import requests

def fetch_price(epoch_timestamp):
    url="http://127.0.0.1:8000"
    route = "/prices"
    params = f'?epoch={epoch_timestamp}'

    resp = requests.get(f'{url}{route}{params}')
    if resp.status_code == 200:
        print(f'Fetched price: {resp.json()}')
        return resp.json().get('price')
    else:
        print('Failed to fetch price')
        return None

