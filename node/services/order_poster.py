import requests
from termcolor import cprint
from ..models.order import Order

def post_order(order: Order):
    url="http://127.0.0.1:8000"
    route = "/orders"

    resp = requests.post(f'{url}{route}', order.to_json())
    if resp.status_code == 200:
        cprint(f"Posting order: {order.quantity}kWh @ ${order.price}/kWh", "red", "on_white", attrs=["reverse", "bold"])
    else:
        print('Failed to post order')
        return None

