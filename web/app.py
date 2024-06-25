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
    query_table = f"FROM v_result"
    query_filter = f"where final_seconds not in ('NS', 'DQ', 'DNF') and swimmer_name like '{swimmer}%'"
    
    #all star query
    union_all_star_query = f" union all SELECT swimmer, year_week as 'week',  CONCAT(d.event_name, ' ', 'All Star') as 'event',  cast(allstar.nom_time_sec as float) as 'final(seconds)',  allstar.nom_time as 'final' FROM v2_YEAR2012_AFT as d join all_star_nom as allstar on d.event_no = allstar.event_no and d.`year` = (select max(year) from v2_YEAR2012_AFT)"

    #modify where filter when stroke is selected
    if stroke != "all":
        query_filter = f"where final_seconds not in ('NS', 'DQ', 'DNF') and swimmer_name like '{swimmer}%' and event_name like '%{stroke}%'"

    #build final query for specific stroke only (not all)
    query = f"{query_columns} {query_table} {query_filter} {union_all_star_query} {query_filter}"
    
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

        #default html page to display
        html = 'display.html'

        #check if dataframe is empty or not
        if not data_values.empty:
             #create title fron the lookup functtion
             #get the last row as the df is ordered by swimmer age
            title = data_values["swimmer"].iloc[-1]
            #create the chart
            fig = px.line(data_values, x="week", y="final(seconds)", color="event", text="final", title=title)
            
            # #use together with scroolZoom, disable zooming in chart
            # fig.update_xaxes(fixedrange=True)
            # fig.update_yaxes(fixedrange=True)

            #to html, hiding all buttons on the top right. To disable zoom only use: 'scrollZoom':False,
            chart_html = fig.to_html(full_html=False, config={'displayModeBar': False})

            #get the user agent of the client device
            user_agent = request.headers.get('User-Agent')

            #check if the user agent is a mobile device
            is_mobile = 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent

            if is_mobile:
                html = 'display_mobile.html'

        else: #this is when dataframe is empty which means no swimmer found
             chart_html = "<h1>Sorry, I can't find your swimmer.</h1>"

        return render_template(html, chart_html=chart_html)

    else:
        #to show index html as starting point
        return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)


