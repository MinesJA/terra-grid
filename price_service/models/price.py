import datetime
from dataclasses import dataclass

@dataclass
class Price:
    """Class for representing a Price"""
    price: float
    timestamp: datetime.datetime

    def to_json(self):
        return {
                'price': self.price, 
                'datetime': self.timestamp.isoformat()
                }

