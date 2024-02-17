import datetime
from operator import itemgetter
from dataclasses import dataclass

@dataclass
class Order:
    """Class for representing an Order"""
    id: int | None 
    posted_at: datetime.datetime
    price: float
    node_id: int
    order_type: str
    quantity: float 

    @classmethod
    def build(cls, json):
        id = json.get('id')
        posted_at = datetime.datetime.fromisoformat(json.get('posted_at'))
        vals = itemgetter('price', 'node_id', 'order_type', 'quantity')(json)
        return cls(id, posted_at,  *vals)


    def to_json(self):
        return {
                'price': self.price, 
                'posted_at': self.posted_at.isoformat(),
                'node_id': self.node_id,
                'order_type': self.order_type,
                'quantity': self.quantity
                }
