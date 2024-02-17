import mariadb
import sys

def connect():
    # Connect to MariaDB Platform
    try:
        print("Trying to connect to MariaDb")
        conn = mariadb.connect(
                user="terra",
                password="terra",
                host="localhost",
                port=3306,
                database="terra"
                )
        print("Connected to MariaDB")
        return conn 
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def create_schema(conn):
    conn.execute("CREATE DATABASE IF NOT EXISTS terra ")
    print("terra database created")

    conn.execute(
            """CREATE TABLE IF NOT EXISTS terra.orders (
                id INT(11) unsigned NOT NULL AUTO_INCREMENT,
                order_type VARCHAR(500) NOT NULL,
                price FLOAT(11) unsigned NOT NULL,
                node_id INT(11) unsigned NOT NULL,
                posted_at DATETIME NOT NULL,
                quantity FLOAT(11) NOT NULL,
                PRIMARY KEY (id)
                )"""
            )
    print("orders table created")

    conn.execute(
            """CREATE TABLE IF NOT EXISTS terra.prices (
                id INT(11) unsigned NOT NULL AUTO_INCREMENT,
                price FLOAT(11) unsigned NOT NULL,
                epoch_timestamp VARCHAR(500) NOT NULL,
                PRIMARY KEY (id),
                CONSTRAINT unique_epochtimestamp UNIQUE (epoch_timestamp)
                )"""
            )
    print("prices table created")

def drop_schema(conn):
    conn.execute("DROP DATABASE terra IF EXISTS")
    print("terra database and orders table dropped")

