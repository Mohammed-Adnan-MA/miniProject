import requests, csv, os
from flask import Flask, render_template, request, jsonify
from flask_api import FlaskAPI
from datetime import datetime
from models import *

app = Flask(__name__)
#app = FlaskAPI(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql://postgres:1234@localhost/miniproject")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/apod", methods=["GET", "POST"])
def pic():
    if request.method == "GET":
        return "<h1>Please submit the form instead.</h1>"
    else:    
        # Get form information.
        date = request.form.get("date")

        res = requests.get("https://api.nasa.gov/planetary/apod?api_key=TF8nfPs2clvAJgslR8ejTgob0X4iw1sjasWZXxkl&",
                        params={"date": date})
                        
        if res.status_code != 200:
            raise Exception(f"{res.status_code} - ERROR: API request unsuccessful.")
        else:
            data = res.json()
            date = data ["date"] 
            explanation = data ["explanation"]
            url = data ["url"]
            try:
                copyrights = data ["copyright"]
            except:
                return render_template("error.html", error="There is no available copyrights for this picture")
            title = data ["title"]


            m = miniproject(date= date, url= url, explanation= explanation, copyrights= copyrights, title= title)
            db.session.add(m)
            db.session.commit()


            return render_template("index.html", date= date, url= url, explanation= explanation,
                                     copyrights= copyrights, title= title, check= "1")

@app.route("/archive")
def archive():
    dbImport= []
    for i in miniproject.query.all():
        dbImport.append(i)
    return render_template ("history.html", dbImport=dbImport)

@app.route("/csv")
def csvIntoDb():
    apod= open("miniProject.csv")
    reader= csv.reader(apod)
    for date, url, explanation, copyrights, title in reader:
        m = miniproject(date= date, url= url, explanation= explanation, copyrights= copyrights, title= title)
        db.session.add(m)
    db.session.commit()
    return ("<h1>Information has been submitted successfully into the database.</h1>")

@app.route("/api/<int:miniproject_id>")
def getApi(miniproject_id):
    getApi = []
    checking = []
    for i in miniproject.query.all():
        if i.id == miniproject_id:
            return jsonify({
                "date": i.date,
                "url": i.url,
                "explanation": i.explanation,
                "copyright": i.copyrights,
                "title": i.title
            })
            
    return jsonify({"error": "Invalid id"}), 422
