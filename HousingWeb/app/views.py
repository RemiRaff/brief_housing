# coding: utf8
from app import app
from flask import render_template, request, abort, redirect, url_for

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from app import models




# C'est ici qu'on demande à notre appli flask d'acheminer toutes les demandes d'URL à la racine vers la fonction index()
# A chaque fois qu'on ouvrira un navigateur pour accéder à l'indexe, c'est cette fonction qui sera appelé
# @app.route est un décorateur de la varibale app qui va encapsuler la fonction index()
# et acheminer les demande vers cette fonction

@app.route('/')
def index():
    return render_template( 'index.html')

@app.route('/dashboard')
def dashboard():
    models.graphique()
    return render_template( 'dashboard.html')

@app.route('/formulaire_predict')
def formulaire_predict():
    return render_template( 'formulaire_predict.html')

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    nop = request.form['ocean']
    mi = request.form['revenu']
    predict = models.predict(mi, nop)
    return render_template( 'predict.html', nop=nop, mi=mi, predict=predict)