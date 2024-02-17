# Terra Grid
A POC of a sharing economy for home battery discharges. Nodes pull prices from the Price Service on a tempo, and based on the current price execute different rules (discharge battery, charge battery). Theoretically allows individuals to participate in the energy market, which would help shore up the grid at time when supply is high or low relative to demand.

Setup
=====
Fork and clone the repo

`cd` into the repo

Start a python virtual environment and activate it:
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies:
```
$ pip install --requirement ./requirements.txt
```

Run
====
## Run the Price Service
```
$ python3 -m price_service.app
```
## Run a Node
```
$python3 -m node.app
```
