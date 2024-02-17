#! /bin/bash

curl -X POST "http://127.0.0.1:8000/orders" --header "Content-Type: application/json" -d @- << EOF
{
    "price": 0.37, 
    "posted_at": "2024-02-15T11:53:45.308579", 
    "node_id": 1, 
    "order_type": "sell" 
} 
EOF
