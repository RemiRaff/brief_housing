# coding: utf8
# Depuis flask on importe la classe Flask qui représente l'application WSGI
# Une application WGI est, pour faire simple, un ensemble de comportement et de méthode
from flask import Flask
from app.config import configuration


# Dans la variable app on va créer une instance d'application et on lui fournit le nom de notre module en cour 
# Cela va permettre à l'application de trouver les ressources dont elle à besoin dans le dossier en cours
# L'instance d'application est le registre central pour les éléments tel que les vues, les itinéraires d'URL, ou les configuration des modèle
# En somme on initialise l'application Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    return app