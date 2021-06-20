#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 14:15:00 2021

@author: simplon
"""
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from base import Base, Session, engine
from prix_med import Prix_Median


def data_split(df_data, random_state=0, test_size=0.2):
    col = df_data.columns
    X = pd.DataFrame()
    for i in range(1,len(col)):
        X[col[i]] = df_data[col[i]]
    y = df_data[col[0]]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def model_SGDR(alpha, max_iter, X_train, y_train):
    "Model SGDRegressor"
    
    model = make_pipeline(StandardScaler(),
                          SGDRegressor(max_iter=max_iter, alpha=alpha))
    model.fit(X_train, y_train)
    
    return model


def model_LR(X_train, y_train):
    "Model Linear Regressor"
    
    model = LinearRegression()
    
    model.fit(X_train, y_train)
    
    return model


def model_RR(alpha, max_iter, l1_ratio, X_train, y_train):
    "Model Regular Regression"
    
    model = make_pipeline(StandardScaler(),
                          SGDRegressor(max_iter=max_iter,
                                       alpha=alpha,
                                       penalty = 'elasticnet',
                                       l1_ratio=l1_ratio))

    model.fit(X_train, y_train)

    return model


def model_PR(alpha, max_iter, degree, X_train, y_train):
    "Polynomial Regression"
    
    model = make_pipeline(StandardScaler(), PolynomialFeatures(degree=degree, include_bias=False),
                          SGDRegressor(max_iter=max_iter, alpha=alpha))

    model.fit(X_train, y_train)

    return model


def metrics_model(model, model_title, X, y):
    return {'modele': model_title,
            'mean_absolute_error': mean_absolute_error(y, model.predict(X)),
            'mean_squared_error': mean_squared_error(y, model.predict(X)),
            'r2_score':r2_score(y, model.predict(X))}

Base.metadata.create_all(engine)

session = Session()

# Test de ML
l_tuple = session.query(Prix_Median.median_house_value,
                        Prix_Median.ocean_proximity_str).all()
#    .filter(Prix_Median.ocean_proximity_str == 'INLAND')
    
l1,l2,l3=[],[],[]
for i in range(len(l_tuple)):
    l1.append(l_tuple[i][0])
    l2.append(l_tuple[i][1])
    # l3.append(l_tuple[i][2])
df_data = pd.DataFrame()
df_data['mhv']=l1
# df_data['2']=l2

# concat colle les lignes, il faut axis=1, éclatement de ocean_proximity avec get_dummies
df_data = pd.concat([df_data,pd.get_dummies(pd.DataFrame(l2))],axis=1)


X_train, X_test, y_train, y_test = data_split(df_data,0)

# result, liste de dictionnaire
ld_result = []

print('Model LR')
ld_result.append(metrics_model(model_LR(X_train, y_train), "Model_LR", X_test, y_test))

print('Model SGDR')
ld_result.append(metrics_model(model_SGDR(0.5, 1000, X_train, y_train), "Model_SGDR_0.5_1k", X_test, y_test))
ld_result.append(metrics_model(model_SGDR(0.1, 750, X_train, y_train), "Model_SGDR_0.1_0.75k", X_test, y_test))
ld_result.append(metrics_model(model_SGDR(0.001, 500, X_train, y_train), "Model_SGDR_0.001_0.5k", X_test, y_test))
ld_result.append(metrics_model(model_SGDR(0.0001,500, X_train, y_train), "Model_SGDR_0.0001_0.5k", X_test, y_test))

df_metrics = pd.DataFrame(ld_result)
ax = sns.barplot(x="modele", y="mean_absolute_error", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="mean_squared_error", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="r2_score", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()

ld_result = []
print('Model Regular regression')
ld_result.append(metrics_model(model_RR(0.0001, 500, 1, X_train, y_train), "Model_Lasso", X_test, y_test))
ld_result.append(metrics_model(model_RR(0.0001, 500, 0.75, X_train, y_train), "Model_Elasticnet_75", X_test, y_test))
ld_result.append(metrics_model(model_RR(0.0001, 500, 0.5, X_train, y_train), "Model_Elacticnet_50", X_test, y_test))
ld_result.append(metrics_model(model_RR(0.0001, 500, 0.25, X_train, y_train), "Model_Elasticnet_25", X_test, y_test))
ld_result.append(metrics_model(model_RR(0.0001, 500, 0, X_train, y_train), "Model_RIDGE", X_test, y_test))

df_metrics = pd.DataFrame(ld_result)
ax = sns.barplot(x="modele", y="mean_absolute_error", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="mean_squared_error", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="r2_score", data=df_metrics)
plt.xticks(rotation=90)
plt.show()
plt.close()

ld_result = []
print('Model Polynimial regression')
ld_result.append(metrics_model(model_PR(0.01, 10000, 2, X_train, y_train), "Model_d2_0.01", X_test, y_test))
ld_result.append(metrics_model(model_PR(0.001, 10000, 2, X_train, y_train), "Model_d2", X_test, y_test))
ld_result.append(metrics_model(model_PR(0.0001, 1000, 2, X_train, y_train), "Model_d3", X_test, y_test))

df_metrics = pd.DataFrame(ld_result)
ax = sns.barplot(x="modele", y="mean_absolute_error", data=df_metrics)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="mean_squared_error", data=df_metrics)
plt.show()
plt.close()
ax = sns.barplot(x="modele", y="r2_score", data=df_metrics)
plt.show()
plt.close()

session.close()