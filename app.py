import flask
from flask import Flask, jsonify, after_this_request, abort, make_response
from flask import render_template, request, send_file, redirect
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
import random as rd
import csv
from tqdm import tqdm
import phases.first_phase       #on sait jamais de combien de librairies on a besoin

# Check for empty strings and convert to integers
def convert_to_int(value):
    return int(value) if isinstance(value, str) and value.strip() else value

# Read TSV file and parse card data
def read_card_data(file_path):
    cards = []
    with open(file_path, 'r', newline='') as mycsv:
        reader = csv.DictReader(mycsv, delimiter='\t')
        for idx, row in enumerate(reader):
            if row['Choix'] == '':
                break

            card = {
                'index': idx,
                'name': row['Choix'],
                'effect_yes_R': convert_to_int(row.get('Oui_R', 0)),
                'effect_yes_C': convert_to_int(row.get('Oui_C', 0)),
                'effect_yes_I': convert_to_int(row.get('Oui_I', 0)),
                'effect_no_R': convert_to_int(row.get('Non_R', 0)),
                'effect_no_C': convert_to_int(row.get('Non_C', 0)),
                'effect_no_I': convert_to_int(row.get('Non_I', 0)),
                'fire_defense': convert_to_int(row.get('feu', 0)),
                'earth_defense': convert_to_int(row.get('terre', 0)),
                'air_defense': convert_to_int(row.get('air', 0)),
                'water_defense': convert_to_int(row.get('eau', 0)),
                'intro': row.get('intro', ''),
                'outro': row.get('outro', '')
            }

            cards.append(card)

    return cards

#Generate the cards only once
cards = read_card_data('./static/cartes_action.tsv')

app = Flask(__name__)
CORS(app)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/session')
def session():
    return render_template("index.html")

@app.route('/identification', methods=['GET','POST'])
def identification():
    success=False
    if request.method=='POST':
        success=True
        id = request.form['number']
        print("Bienvenue ", id)
    else:
        number = request.args.get('number')
        if number==None:
            return redir
        success=True
        print("Je sais déjà que tu es : ",number)
    resp = jsonify(success=success)
    return render_template("index.html")

# Flask endpoint to serve card data
@app.route('/api/cards')
def get_cards():
    return jsonify({'cards': cards})
    
if __name__ == '__main__':
    app.run(port=5000)

