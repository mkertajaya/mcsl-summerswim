from flask import Flask
from flask import render_template, request


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #fetch form data
        swimmerdata = request.form
        name = swimmerdata["swimmer"]
        stroke = swimmerdata["stroke"]
        before_2012 = swimmerdata["year"]
        return f"Swimmer name is: {name}, stroke is: {stroke} \
            and before 2012 is: {before_2012}"
    return render_template("home.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)