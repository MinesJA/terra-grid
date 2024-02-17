import falcon
import datetime
import random
import json
import traceback 

# def populate_prices():
#     d = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=30)
#     price_vals = {d: 0.20}
#
#     for x in range(120):
#       t = d + datetime.timedelta(minutes=x) 
#       price_vals[t] = round(random.uniform(0.20, 0.50), 2) 
#
#     return price_vals
#
# PRICE_VALS = populate_prices() 

class PriceResource():
    
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def on_get(self, req, resp):
        """Fetches the next day price for a given 
        time.

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
            datetime (str): datetime of the next day price
        """
        try:
            epoch = req.get_param_as_int('epoch', required=True, min_value=0)
            # d = datetime.datetime.fromtimestamp(epoch)
            cur = self.db_conn.cursor()
            print(epoch)
            cur.execute("SELECT * FROM prices WHERE epoch_timestamp = %s", [epoch])

            for (_, price, _) in cur:
                d = datetime.datetime.fromtimestamp(epoch).isoformat()
                price_data = {'price': price, 'datetime': d}
                print(f'Fetching price for datetime: {datetime} | price_data: {price_data}')

                resp.text = json.dumps(price_data)
                resp.status = falcon.HTTP_200

        except:
            print(traceback.format_exc())            
