from .db import connect, create_schema
import datetime
import random

def populate_prices(cur):
    d = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=30)

    for x in range(60000):
        t = d + datetime.timedelta(minutes=x)
        price = round(random.uniform(0.20, 0.50), 2) 

        sql = """INSERT IGNORE INTO prices (epoch_timestamp, price) VALUES (?, ?)"""

        cur.execute(sql, (t.strftime('%s'),  price))

if __name__ == "__main__":
    conn = connect()
    print(f'Connected to db {conn}')
    create_schema(conn.cursor()) 

    populate_prices(conn.cursor())
    conn.commit()
