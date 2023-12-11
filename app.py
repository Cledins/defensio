import flask
from flask import Flask, jsonify, after_this_request, abort, make_response
from flask import render_template, request, send_file, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
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
    if value != '':
        return(int(value)) 
    else:
        return 0

# Read TSV file and parse card data
def read_card_data(file_path):
    cards = []
    with open(file_path, 'r', newline='', encoding='utf-8') as mycsv:
        reader = csv.DictReader(mycsv, delimiter='\t')
        for idx, row in enumerate(reader):
            if row['Choix'] == '':
                break

            card = {
                'index': idx,
                'name': row['Choix'],
                'effect_yes_R':  convert_to_int(row['Oui_R']),
                'effect_yes_C': convert_to_int(row['Oui_C']),
                'effect_yes_I': convert_to_int(row['Oui_I ']),
                'effect_no_R': convert_to_int(row['Non_R']),
                'effect_no_C': convert_to_int(row['Non_C ']),
                'effect_no_I': convert_to_int(row['Non_I ']),
                'fire_defense': convert_to_int(row['feu']),
                'earth_defense': convert_to_int(row['terre']),
                'air_defense': convert_to_int(row['air']),
                'water_defense': convert_to_int(row['eau']),
                'intro': row.get('intro', ''),
                'outro': row.get('outro', '')
            }

            cards.append(card)
    return cards

def create_app():
    from database.table import UserMetrics
    basedir = os.path.abspath(os.path.dirname(__file__))

    #Generate the cards only once
    cards = read_card_data('./static/cartes_action.tsv')

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.db')}"
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    @app.route('/')
    def login():
        return render_template("login.html")

    #débrief1
    @app.route('/debrief1')
    def debrief1():
        return render_template("debrief1.html")

    @app.route('/session', methods=['GET','POST'])
    def identification():
        success=False
        if request.method=='POST':
            success=True
            id = request.form['number']
            nouvelles_metrics = UserMetrics(
                id=int(id),
                jauge_i=30,
                jauge_r=30,
                jauge_c=30,
                jauge_4=30
            )
            #db.session.add(nouvelles_metrics)
            #db.session.commit()

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

    with app.app_context():
        meta = db.metadata
        #if not inspect(db.engine).has_table(UserMetrics.__tablename__):
        db.create_all()
          #  print("oui", inspect(db.engine))
        print("non",inspect(db.engine).has_table(UserMetrics.__tablename__) )

    @app.route('/get-jauge/<user>')
    def getjauge(user):
        print("non",inspect(db.engine).has_table(UserMetrics.__tablename__) )
        userMetrics = db.session.query(UserMetrics).get(user)
        return jsonify({'jauge_c': userMetrics.jauge_c, 'jauge_i': userMetrics.jauge_i, 'jauge_r':userMetrics.jauge_r, 'jauge_4':userMetrics.jauge_4})

    @app.route('/put-jauge/<user>', methods=['PUT'])
    def putjauge(user):
        userMetrics = db.session.query(UserMetrics).get(user)

        if userMetrics:
            data = request.get_json()

            userMetrics.jauge_i += data.get('jauge_i', 0)
            userMetrics.jauge_r += data.get('jauge_r', 0)
            userMetrics.jauge_c += data.get('jauge_c', 0)
            userMetrics.jauge_4 += data.get('jauge_4', 0)

            db.session.commit()

            return jsonify({'message': 'UserMetrics updated successfully'})
        else:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

    @app.route('/reset-jauge/<user>')
    def resetjauge(user):
        userMetrics = db.session.query(UserMetrics).get(user)

        if userMetrics:
            userMetrics.jauge_i = 30
            userMetrics.jauge_r = 30
            userMetrics.jauge_c = 30
            userMetrics.jauge_4 = 30

            db.session.commit()

            return jsonify({'message': 'UserMetrics updated successfully'})
        else:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

    return app


class Base(DeclarativeBase):
   pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()


if __name__ == '__main__':
    app = create_app()
    app.run(port=10407)


