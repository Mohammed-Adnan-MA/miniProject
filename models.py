import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class miniproject(db.Model):
    __tablename__ = "mini_project"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    url = db.Column(db.String, nullable=False)
    explanation = db.Column(db.String, nullable=False)
    copyrights = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)

'''    def __init__(self, date, url, explanation, copyrights, title):
        self.date= date
        self.url= url 
        self.explanation= explanation 
        self.copyrights= copyrights  
        self.title=title
    
    def add_to(self, date, url, explanation, copyrights, title):
        #m = miniproject(date= date, url=url, explanation=explanation, copyrights= copyrights, title=title)'''
