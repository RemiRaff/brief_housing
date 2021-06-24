# coding: utf8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from joblib import load

from app.base import Base, Session, engine
from app.prix_med import Prix_Median


def graphique():
    Base.metadata.create_all(engine)
    session = Session()
    # data est une liste de tuple
    data = session.query(Prix_Median.longitude,
                         Prix_Median.latitude,
                         Prix_Median.housing_median_age,
                         Prix_Median.total_rooms,
                         Prix_Median.total_bedrooms,
                         Prix_Median.population,
                         Prix_Median.households,
                         Prix_Median.median_income,
                         Prix_Median.median_house_value,
                         Prix_Median.ocean_proximity_str).all()
    session.close()

    df_data = pd.DataFrame(data).dropna()

    palette=sns.color_palette("Paired")
    sns.set_palette(palette)

    plt.figure(figsize=[15,20])
    plt.gcf().subplots_adjust(wspace = 0.5, hspace = 0.5)

    plt.subplot(421)
    sns.scatterplot(data=df_data, x="longitude", y="latitude", hue='median_house_value')
    plt.title("Distribution géographique des prix médians")
    plt.xticks(rotation=45)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.axis("scaled")

    plt.subplot(422)
    sns.scatterplot(data=df_data, x="median_house_value", y="median_income", hue='ocean_proximity_str')
    plt.title("Distribution des prix médians suivant les salaires médians")
    plt.xticks(rotation=45)
    plt.xlabel('Prix médians en $')
    plt.ylabel('Salaires médians')

    plt.subplot(423)
    sns.distplot(df_data["total_rooms"])
    plt.title("Distribution des biens suivant leur surface totale (inch/m2)")
    plt.xticks(rotation=45)
    plt.xlim(0, 12000)
    plt.xlabel('Surface totale en inch/m2')

    plt.subplot(424)
    sns.distplot(df_data["total_bedrooms"])
    plt.title("Distribution des biens suivant la surface des chambres (inch/m2)")
    plt.xticks(rotation=45)
    plt.xlim(0, 2000)
    plt.xlabel('Surface chambres en inch/m2')

    plt.subplot(425)
    sns.distplot(df_data["population"])
    plt.title("Distribution des biens suivant la population")
    plt.xticks(rotation=45)
    plt.xlim(0, 4000)
    plt.xlabel('Polulation')

    plt.subplot(426)
    sns.distplot(df_data["households"])
    plt.title("Distribution des biens suivant le nb de foyer du quartier")
    plt.xticks(rotation=45)
    plt.xlim(0, 2000)
    plt.xlabel('Nb de foyer')

    plt.subplot(427)
    sns.distplot(df_data["median_income"])
    plt.title("Distribution des biens sur les revenus médians")
    plt.xticks(rotation=45)
    # plt.xlim(0, 600000)
    plt.xlabel('Revenu médian en m$')

    plt.subplot(428)
    sns.distplot(df_data["housing_median_age"])
    plt.title("Distribution des biens suivant leur age médian")
    plt.xticks(rotation=45)
    # plt.xlim(0, 300000)
    plt.xlabel('Age médian')

    plt.savefig("app/static/Image/dashboard.png")
    
    return None


def predict(mi, nop):
    # load model et return prediction
    model = load('app/model_poly.joblib')
    x = model.predict([[mi, nop]])[0]
    return round(x,2)