import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

# Connect to the Sakila database
engine = create_engine('mysql://root:@localhost/sakila')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Sakila Rental Data Over Time"),
    
    # Dropdown to select a category
   # Dropdown to select a category
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'Category 1', 'value': 1},
            {'label': 'Category 2', 'value': 2}
            # Add more options based on your data
        ], value=1),
    
    # Line chart to display data over time
    dcc.Graph(id='line-chart'),
    dcc.Graph(id="plot-chart"),
    dcc.Graph(id="part-chart"), 
    dcc.Graph(id="plot-chart2"),
    dcc.Graph(id="plot-chart3")
    
])

# Define callback to update the line chart based on the selected category
#EXCERICE 1
@app.callback(
    Output('line-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    query = """
        SELECT DISTINCT c.first_name, c.last_name
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        WHERE cat.name = 'Family';
        """

    rental_data = pd.read_sql(query, engine) if query is not None else pd.DataFrame()

    fig = {
        'data': [
            {
                'x': rental_data.iloc[:, 0] if not rental_data.empty else [],
                'y': rental_data.iloc[:, 1] if not rental_data.empty else [],
                'type': 'bar',
                'marker': {'color': 'green'}  # Adjust color for different exercises
            }
        ],
        'layout': {
            'title': f'Data for Exercise {selected_category}',
            'xaxis': {'title': 'X-axis title'},
            'yaxis': {'title': 'Y-axis title'}
        }
    }

    return fig




# Define callback to update the line chart based on the selected category
#EXCERICE 2
@app.callback(
    Output('plot-chart', 'figure'),
    [Input('category-dropdown', 'value')]
)

def update_plot_chart(selected_category):
    query = """
        SELECT f.title, SUM(p.amount) as total_revenue
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY f.title
        ORDER BY total_revenue DESC
        LIMIT 5;
        """
    

    rental_data = pd.read_sql(query, engine) if query is not None else pd.DataFrame()

    fig = {
        'data': [
            {
                'x': rental_data.iloc[:, 0] if not rental_data.empty else [],
                'y': rental_data.iloc[:, 1] if not rental_data.empty else [],
                'type': 'bar',  # Change the type to 'bar'
                'marker': {'color': 'blue'}  # Adjust color for different exercises
            }
        ],
        'layout': {
            'title': f'Data for Exercise {selected_category}',
            'xaxis': {'title': 'Film Title'},  # Adjust the x-axis title
            'yaxis': {'title': 'Total Revenue'}  # Adjust the y-axis title
        }
    }

    return fig

#EXCERICE 4
@app.callback(
    Output('part-chart', 'figure'),
    [Input('category-dropdown', 'value')]
    )

def update_plot_chart3(selected_category):
    query = """
        SELECT c.first_name as first_name, c.last_name, SUM(p.amount) as total_payments
        FROM customer c
        JOIN payment p ON c.customer_id = p.customer_id
        GROUP BY c.customer_id
        ORDER BY total_payments DESC;
        """

    total_payments = pd.read_sql(query, engine) if query is not None else pd.DataFrame()
    print(total_payments)
    fig = {
    'data': [
        {
            'x': total_payments['first_name'],
            'y': total_payments['total_payments'],
            'type': 'bar', # Change the type to 'bar'
            'marker': {'color': 'blue'} # Adjust color for different exercises
        }
        ],
        'layout': {
            'title': f'Data for Exercise {selected_category}',
            'xaxis': {'title': 'Customer Name'}, # Adjust the x-axis title
            'yaxis': {'title': 'Total Payments'} # Adjust the y-axis title
        }
}
    return fig


#EXCERISE 3
@app.callback(
    Output('plot-chart2', 'figure'),
    [Input('category-dropdown', 'value')]
    )

def update_plot_chart2(selected_category):
    query = """
        SELECT a.first_name, a.last_name, COUNT(*) as film_appearances
        FROM actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        GROUP BY a.actor_id
        HAVING film_appearances > 15;
        """
    total_actors = pd.read_sql(query, engine) if query is not None else pd.DataFrame()
    print(total_actors)

    fig = {
    'data': [
        {
            'x': total_actors['first_name'] + ' ' + total_actors['last_name'],  # Concatenate first and last names
            'y': total_actors['film_appearances'],
            'type': 'bar', # Change the type to 'bar'
            'marker': {'color': 'blue'} # Adjust color for different exercises
        }
        ],
        'layout': {
            'title': f'Data for Exercise {selected_category}',
            'xaxis': {'title': 'Actor Names'}, # Adjust the x-axis title
            'yaxis': {'title': 'Quantity of Films'} # Adjust the y-axis title
        }
}
    return fig



#EXCERISE 3
@app.callback(
    Output('plot-chart3', 'figure'),
    [Input('category-dropdown', 'value')]
    )

def update_plot_chart3(selected_category):
    query = """
        SELECT cat.name, f.title, f.rating
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        WHERE f.rating = 'G' OR f.rating = 'PG'
        ORDER BY cat.name, f.title;

        """
    total_films = pd.read_sql(query, engine) if query is not None else pd.DataFrame()
    print(total_films)

    fig = {
    'data': [
        {
            'x': total_films['title'],
            'y': total_films['rating'],
            'type': 'bar', # Change the type to 'bar'
            'marker': {'color': 'blue'} # Adjust color for different exercises
        }
        ],
        'layout': {
            'title': f'Data for Exercise {selected_category}',
            'xaxis': {'title': 'Film Names'}, # Adjust the x-axis title
            'yaxis': {'title': 'Ratings'} # Adjust the y-axis title
        }
}
    return fig



app.run_server(debug=True)