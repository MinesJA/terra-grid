import datetime
import random

AVG_DAILY_KWH_USAGE = 30

def populate_energy_values():
    d = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=30)
    epoch = d.strftime('%s')

    per_min = round(AVG_DAILY_KWH_USAGE/(24*60), 2)
    energy_vals = {epoch: per_min}

    for x in range(120):
        t = d + datetime.timedelta(minutes=x) 
        e = t.strftime('%s')
        energy_vals[e] = round(random.uniform(per_min-5, per_min+5), 2) 

    return energy_vals

ENERGY_VALS = populate_energy_values()

def fetch_energy(epoch_timestamp):
    energy = ENERGY_VALS.get(epoch_timestamp)
    d = datetime.datetime.fromtimestamp(int(epoch_timestamp))
    vals = {'energy': energy, 'datetime': d.strftime("%Y-%m-%d %H:%M:%S")}
    print(f"Fetching energy: {vals}") 
    return energy

