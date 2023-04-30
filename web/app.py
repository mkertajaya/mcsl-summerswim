from flask import Flask, render_template, request
import pandas as pd
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
    query_columns = f"SELECT  swimmer, year_week as 'week', event_name as 'event',cast(final_seconds as float) as 'final(seconds)', final"
    query_table = f"FROM v2_YEAR2012_AFT"
    query_filter = f"where final_seconds not in ('NS', 'DQ', 'DNF') and swimmer_name like '{data}%'"
    query_orderby = f"order by swimmer_age"
    query = f"{query_columns} {query_table} {query_filter} {query_orderby}"
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the data to a Pandas dataframe
    df = pd.DataFrame(results, columns=["swimmer", "week", "event", "final(seconds)", "final"])

    # Close the database connection
    cursor.close()
    db.close()

    # Return the data as a Pandas dataframe
    return df



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve the form data
        data = request.form["swimmer"]

        # Lookup the data in the database
        data_values = lookup_data(data)

        #create title fron the lookup functtion
        #get the last row as the df is ordered by swimmer age
        title = data_values["swimmer"].iloc[-1]

        # Create the chart
        fig = px.line(data_values, x="week", y="final(seconds)", color="event", text="final",markers=True, title=title)

        # Return the chart as an HTML string
        return fig.to_html(full_html=False)
    else:
        return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)


