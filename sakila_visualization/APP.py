import influxdb_client
import os
import time
import pymysql

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Sakila MySQL database connection
mysql_connection = pymysql.connect(
    host='localhost',
    user='root:@localhost',
    password='',
    database='sakila'
)

# InfluxDB connection
token = os.environ.get("INFLUXDB_TOKEN")
org = "Trini"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "Trini"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Fetch data from MySQL and write to InfluxDB
with mysql_connection.cursor() as cursor:
    cursor.execute("""
        SELECT c.first_name as first_name, c.last_name, SUM(p.amount) as total_payments
        FROM customer c
        JOIN payment p ON c.customer_id = p.customer_id
        GROUP BY c.customer_id
        ORDER BY total_payments DESC;
    """)
    rows = cursor.fetchall()

for row in rows:
    point = (
        Point("measurement1")
        .tag("first_name", row[0])
        .tag("last_name", row[1])
        .field("total_payments", row[2])
    )
    write_api.write(bucket=bucket, org="Trini", record=point)
    time.sleep(1)  # Separate points by 1 second

query_api = write_client.query_api()

query = """from(bucket: "Trini")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="Trini")

for table in tables:
    for record in table.records:
        print(record)
