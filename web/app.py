from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import mysql.connector
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

def lookup_data(data):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # Retrieve the data from the database
    query = f"SELECT swimmer, week, substring(event, POSITION('-' IN event)+2, 100) as 'event',cast(final_seconds as float) as time FROM YEAR2022 where swimmer_name like '{data}%'"
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the data to a Pandas dataframe
    df = pd.DataFrame(results, columns=["swimmer", "week", "event", "time"])

    # Close the database connection
    cursor.close()
    db.close()

    # Return the data as a Pandas dataframe
    return df



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve the form data
        data = request.form["data"]

        # Lookup the data in the database
        data_values = lookup_data(data)

        #create title fron the lookup functtion
        title = data_values["swimmer"][0]

        # Create the chart
        fig = px.line(data_values, x="week", y="time", color="event", markers=True, title=title)

        # Return the chart as an HTML string
        return fig.to_html(full_html=False)
    else:
        return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)

