from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

app = Flask(__name__)

#read json config file
with open("config.json") as json_data_file:
    data = json.load(json_data_file)
    # Define your MySQL database connection details
    db_host = data["mysql"]["db_host"]
    db_user = data["mysql"]["db_user"]
    db_password = data["mysql"]["db_password"]
    db_name = data["mysql"]["db_name"]


# Function to retrieve data from the database
def get_data(text_input, checkbox1_input, checkbox2_input):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Retrieve the data from the database
    cursor = db.cursor()

    # Construct the SQL query
    query = "SELECT x, y1, y2 FROM mytable WHERE text=%s AND "
    params = [text_input]
    
    if checkbox1_input:
        query += "y1 IS NOT NULL"
    else:
        query += "y1 IS NULL"
    if checkbox2_input:
        query += " AND y2 IS NOT NULL"
    else:
        query += " AND y2 IS NULL"
    
    # Execute the query and retrieve the results
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    db.close()
    
    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(data, columns=['x', 'y1', 'y2'])
    
    return df

# Function to generate the plot
def generate_plot(df, checkbox1_input, checkbox2_input):
    # Create a plotly figure with two subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
    
    # Add a trace for the first checkbox if selected
    if checkbox1_input:
        fig.add_trace(
            go.Scatter(x=df['x'], y=df['y1'], mode='lines', name='y1'),
            row=1, col=1
        )
    
    # Add a trace for the second checkbox if selected
    if checkbox2_input:
        fig.add_trace(
            go.Scatter(x=df['x'], y=df['y2'], mode='lines', name='y2'),
            row=2, col=1
        )
    
    # Update the layout
    fig.update_layout(
        title='My Plot',
        xaxis_title='X',
        yaxis_title='Y',
        height=600,
        width=800
    )
    
    return fig

# Define the main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the form data
        text_input = request.form.get('text_input')
        checkbox1_input = request.form.get('checkbox1_input') == 'on'
        checkbox2_input = request.form.get('checkbox2_input') == 'on'
        
        # Retrieve the data from the database
        df = get_data(text_input, checkbox1_input, checkbox2_input)
        
        # Generate the plot
        fig = generate_plot(df, checkbox1_input, checkbox2_input)
        
        # Render the template with the plot
        return render_template('index.html', plot=fig.to_html(full_html=False))
    
    # Render the initial template with an empty plot
    return render_template('index.html', plot='')

if __name__ == '__main__':
    app.run(debug=True)
