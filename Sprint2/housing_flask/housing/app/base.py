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


def connect_db(dico):

    str_engine = (
        dico["connector"]
        + "://"
        + dico["user"]
        + ":"
        + dico["pwd"]
        + "@"
        + dico["host"]
        + ":"
        + dico["port"]
        + "/"
        + dico["bdd"]
    )
    connect = create_engine(str_engine)
    return connect


d = {
    "connector": "postgresql",
    "user": "luca",
    "pwd": "simplon",
    "host": "localhost",
    "port": "5432",
    "bdd": "housing",
}

engine = connect_db(d)*

Session = sessionmaker(bind=engine)

Base = declarative_base()