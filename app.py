import flask
from flask import Flask, jsonify, after_this_request, abort, make_response
from flask import render_template, request, send_file
import re
import os
import sys
import pickle
from sqlitedict import SqliteDict
from flask_cors import CORS
from flask import Response
import traceback 
import requests
import json 
import phases.first_phase       #on sait jamais de combien de librairies on a besoin

app = Flask(__name__)
CORS(app)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/session')
def session():
    return render_template("index.html")

@app.route('/identification', methods=['POST'])
def identification():
    id = request.form['number']
    print(id)
    return('', 200)

    
if __name__ == '__main__':
    app.run(port=5000)

