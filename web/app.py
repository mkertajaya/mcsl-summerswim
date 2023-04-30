from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import mysql.connector
import json


app = Flask(__name__)

#read json config file
with open("config.json") as json_data_file:
    data = json.load(json_data_file)
    # define  MySQL database connection details
    db_host = data["mysql"]["db_host"]
    db_user = data["mysql"]["db_user"]
    db_password = data["mysql"]["db_password"]
    db_name = data["mysql"]["db_name"]

def lookup_data(swimmer, stroke):
    # connect to the MySQL database
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )


    # default query
    query_columns = f"SELECT  swimmer, year_week as 'week', event_name as 'event', cast(final_seconds as float) as 'final(seconds)', final"
    query_table = f"FROM v2_YEAR2012_AFT"
    query_filter = f"where final_seconds not in ('NS', 'DQ', 'DNF') and swimmer_name like '{swimmer}%'"
    query_orderby = f"order by swimmer_age"

    #modify where filter when stroke is selected
    if stroke != "all":
        query_filter = f"where final_seconds not in ('NS', 'DQ', 'DNF') and swimmer_name like '{swimmer}%' and event_name like '%{stroke}%'"

    #build final query
    query = f"{query_columns} {query_table} {query_filter} {query_orderby}"

    #run query
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # convert the data to a Pandas dataframe
    df = pd.DataFrame(results, columns=["swimmer", "week", "event", "final(seconds)", "final"])
    df = df.sort_values(by = ["week"])

    # close the database connection
    cursor.close()
    db.close()

    # return the data as a Pandas dataframe
    return df



@app.route("/", methods=["GET", "POST"])
def home():
    #for post method
    if request.method == "POST":

        # Retrieve the form data (swimmer and stroke)
        swimmer = request.form.get("swimmer")
        stroke = request.form.get("stroke")

        #check if swimmer is blank
        if not swimmer:
            swimmer = 'empty'

        #check if stroke is blank
        if not stroke:
            stroke = 'all'

        # lookup the data in the database
        # and creat dataframe
        data_values = lookup_data(swimmer, stroke)

        #check if dataframe is empty or not
        if not data_values.empty:
             #create title fron the lookup functtion
             # #get the last row as the df is ordered by swimmer age
             title = data_values["swimmer"].iloc[-1]
            # create the chart
             fig = px.line(data_values, x="week", y="final(seconds)", color="event", text="final",markers=True, title=title)
             chart_html = fig.to_html(full_html=False)
        else:
             #handle the case where the dataframe is empty
             chart_html = "<h1>Sorry, I can't find your swimmer.</h1>"
        return chart_html

    else:
        #to show index html as starting point
        return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)


