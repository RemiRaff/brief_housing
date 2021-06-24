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

engine = connect_db(d)
Base = declarative_base()

Session = sessionmaker(bind=engine)
