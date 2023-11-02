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
org = "trini"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "trini"
write_api = write_client.write_api(write_options=SYNCHRONOUS)


# Initialize SQLAlchemy engine for MySQL
engine = create_engine('mysql://root:@localhost/sakila')

# Your SQL query
query = """
SELECT customer_id, count(*) as num_rentals 
FROM rental 
GROUP BY customer_id 
ORDER BY num_rentals desc 
LIMIT 5; 
"""

data = pd.read_sql(query, engine)



points = []
# Create a point for each data row
for row in data.itertuples(index=False):
    point = Point("rental").tag("customer_id", row.customer_id).field("num_rentals", row.num_rentals)
    points.append(point)
# Write points to InfluxDB

# Write points to InfluxDB
write_api.write(bucket=bucket, record=points, write_precision=WritePrecision.NS)


# Close the client
client.close()