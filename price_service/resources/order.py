import falcon
from termcolor import colored, cprint
import traceback
from ..models.order import Order

class OrderResource():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def on_get(self, req, resp):
        """Get order
        """
        try:
            sql = ("SELECT * FROM orders;")
            cursor = self.db_conn.cursor()
            cursor.execute(sql)

            for(id, order_type, price, node_id, posted_at, quantity) in cursor:
                print(f"id: {id}, order_type: {order_type}, price: {price}, node_id: {node_id}, posted_at: {posted_at}, quantity: {quantity}")

            resp.status = falcon.HTTP_200
        except:
            print(traceback.format_exc())            

    async def on_post(self, req, resp):
        """Posts order

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
        """
        try:
            doc = await req.get_media()
            order = Order.build(doc)
            cprint(f"Posting order: {order.quantity}kWh @ {order.price}", "red", "on_white", attrs=["reverse", "bold"])
            sql = """INSERT INTO orders (posted_at, price, node_id, order_type, quantity)
                        VALUES (?, ?, ?, ?, ?)"""

            cur = self.db_conn.cursor()

            cur.execute(sql, (order.posted_at.strftime('%Y-%m-%d %H:%M:%S'), order.price, order.node_id, order.order_type, order.quantity))
            self.db_conn.commit() 
            resp.status = falcon.HTTP_200
        except:
            print(traceback.format_exc())            
