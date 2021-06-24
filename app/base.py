#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:45:44 2021

@author: simplon
"""

# pip install psycopg2-binary
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

import json

with open('./app/.config.json', 'r') as fichier:
    data = json.load(fichier)

db_string = data["connector"]+"://"+data['user']+":"+data['pwd']+"@"+data['host']+':'+data['port']+'/'+data['bd']


engine = create_engine(db_string)


Session = sessionmaker(bind=engine)

Base = declarative_base()