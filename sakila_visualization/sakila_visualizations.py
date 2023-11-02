from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
# Replace 'username' and 'password' with your MySQL username and password
engine = create_engine('mysql://root:@localhost/sakila')
# Exercise 1 visualization
query_1 = """
SELECT DISTINCT c.first_name, c.last_name
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
WHERE cat.name = 'Family';
"""
customer_data = pd.read_sql(query_1, engine)
plt.figure(figsize=(10, 6))
plt.bar(customer_data['first_name'] + ' ' + customer_data['last_name'], 1)
plt.title('Customers who Rented Movies in the "Family" Category')
plt.xlabel('Customer Name')
plt.ylabel('Rental Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



