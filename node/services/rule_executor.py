from .energy_fetcher import fetch_energy
from termcolor import cprint
from .price_fetcher import fetch_price
from .order_poster import post_order
from ..utils.time_utils import get_epoch_timestamp
from ..models.order import Order

def rule_a(node_id, net_energy, curr_price):
    return node_id == 1 and net_energy > 0 and curr_price > 0.10 and curr_price < 0.40

def rule_b(node_id, net_energy, curr_price):
    return node_id == 2 and net_energy > 0 and curr_price > 0.30 and curr_price < 0.40

def rule_c(node_id, net_energy, curr_price):
    return node_id == 3 and net_energy < 0 and curr_price > 0.10 and curr_price < 0.30

def rule_d(node_id, net_energy, curr_price):
    return node_id == 4 and net_energy < 0 and curr_price > 0.10 and curr_price < 0.30

def rule_e(node_id, net_energy, curr_price):
    return node_id == 4 and net_energy > 0 and curr_price > 0.30 and curr_price < 0.40

def discharge_battery(node_id, timestamp, net_energy, curr_price):
    order = Order(
            id=None, 
            node_id=node_id, 
            quantity=net_energy, 
            posted_at=timestamp, 
            price=curr_price, 
            order_type="sell") 
    cprint(f"Discharing Battery: {order.quantity}kWh", "black", "on_light_red", attrs=["dark", "bold"])
    post_order(order)


def charge_battery(node_id, timestamp, net_energy, curr_price):
    order = Order(
            id=None, 
            node_id=node_id, 
            quantity=abs(net_energy), 
            posted_at=timestamp, 
            price=curr_price, 
            order_type="buy") 
    cprint(f"Charing Battery: {order.quantity}kWh", "black", "on_light_green", attrs=["dark", "bold"])
    post_order(order)


RULES = [
        {'name': 'Discharge Node 1 Battery', 'condition': rule_a, 'action': discharge_battery},
        {'name': 'Discharge Node 2 Battery ', 'condition': rule_b, 'action': discharge_battery},
        {'name': 'Charge Node 3 Battery', 'condition': rule_c, 'action': charge_battery},
        {'name': 'Charge Node 4 Battery', 'condition': rule_d, 'action': charge_battery},
        {'name': 'Discharge Node 4 Battery', 'condition': rule_e, 'action': discharge_battery},
        ]

def fetch_rule(node_id, net_energy, curr_price):
    print(f'Net Energy: {net_energy} | Current Price {curr_price}')
    rule = next((x for x in RULES if x['condition'](node_id, net_energy, curr_price)), None)
    if rule:
        print(f'Found rule {rule["name"]}')
        return rule
    else:
        print('No rule found that matches those conditions')
        return None

def execute_rule(rule, node_id, timestamp, net_energy, curr_price):
    print(f'Executing rule {rule["name"]}')
    rule['action'](node_id, timestamp, net_energy, curr_price)

def execute_transaction(node_id, timestamp):
    print("\t")
    cprint(f"=====Executing for timestamp {timestamp}========", "blue")
    epoch_timestamp = get_epoch_timestamp(timestamp)

    net_energy = fetch_energy(epoch_timestamp)
    curr_price = fetch_price(epoch_timestamp)

    rule = fetch_rule(node_id, net_energy, curr_price)
    if rule: execute_rule(rule, node_id, timestamp, net_energy, curr_price)


