#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:42:28 2021

@author: simplon
"""
# pip install psycopg2-binary
# DB housing créée dans pgAdmin
import pandas as pd


from base import Base, Session, engine
from prix_med import Prix_Median


def initialize_db(s):
    filename = "housing.csv"
    filepath = "/home/simplon/Documents/Brief_02_agile/"
    data = pd.read_csv(filepath+filename)
    
    l_ocean_proximity = data['ocean_proximity'].drop_duplicates().tolist() # l.index()
    
    for i in range(data.shape[0]):
        pm = Prix_Median(data.iloc[i]['longitude'],
                         data.iloc[i]['latitude'],
                         data.iloc[i]['housing_median_age'],
                         data.iloc[i]['total_rooms'],
                         data.iloc[i]['total_bedrooms'],
                         data.iloc[i]['population'],
                         data.iloc[i]['households'],
                         data.iloc[i]['median_income'],
                         data.iloc[i]['median_house_value'],
                         l_ocean_proximity.index(data.iloc[i]['ocean_proximity']),
                         data.iloc[i]['ocean_proximity'])
        s.add(pm)
    s.commit()


Base.metadata.create_all(engine)

session = Session()

# Crée et remplit la table de la DB (qui faut la créer sur pgAdmin)
initialize_db(session)

session.close()
