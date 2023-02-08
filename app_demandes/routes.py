# python library
import dill as pickle
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
from plotly import graph_objs as go
import plotly.io as pio
import statsmodels.api as sm
# generer un random number
import uuid
# flask library
from app_demandes import app
from app_demandes.forms import SalaireForm
from flask import render_template, request, session, redirect, url_for
from flask import flash

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])
# for save image on static
file_ = r"C:\Users\daian\anaconda3\envs\salaire\Lib\site-packages\plotly\package_data\plotly.min.js"
pio.kaleido.scope.plotlyjs = file_


@app.route('/')
@app.route('/index')
def index():
    projets = {'titre': 'Simple App pour la prévision du taux salarial'}
    return render_template('index.html', title="Accueil", mod=projets)


pred_as_str = ''
path = ''


@app.route('/form_projet_input', methods=['POST', 'GET'])
def form_projet_input():
    projet_form = SalaireForm()
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('form_projet_input.html', title='Edition projet', form=projet_form,
                               href="static/prediction.png")
    else:
        request_type_str == 'POST'
        _model = pickle.load(open("app_demandes/model.pkl", 'rb'))
        scaler = pickle.load(open("app_demandes/scaler.pkl", 'rb'))
        explainer = pickle.load(open("app_demandes/explainer.pkl", 'rb'))
        salaire_employe_ = pickle.load(open("app_demandes/salaire_employe_train.pkl", 'rb'))

        # annee = projet_form.Annee.data
        # region = projet_form.region.data
        # profession = projet_form.profession.data
        # genre = projet_form.genre.data
        # groupe = projet_form.groupe.data
        # type_emploi = projet_form.type_emploi.data

        test_input = [[projet_form.Annee.data, projet_form.region.data, projet_form.profession.data,
                       projet_form.genre.data, projet_form.groupe.data, projet_form.type_emploi.data]]
        # dataframe with record of request
        X_ = pd.DataFrame(np.array(test_input).reshape(1, -1),
                          columns=["Annee", 'Regions', 'CNP', 'Sexe', "Groupe d'âge", "Genre de travail"])
        X_['Annee'] = X_['Annee'].astype(int)

        # using encoding for categorical variable
        encoder_df = pd.DataFrame(
            scaler.transform(np.array(X_[['Regions', 'CNP', 'Sexe', "Groupe d'âge", 'Genre de travail']]))).set_index(
            X_.index)
        final_df = X_.join(encoder_df)
        final_df.drop(columns=['Regions', 'CNP', 'Sexe', "Groupe d'âge", 'Genre de travail'], axis=1, inplace=True)

        # prediction model
        pred = np.round(np.exp(_model.predict(final_df)), 2)

        # save image graph prediction in static folder
        global path
        random_string = uuid.uuid4().hex
        path = "app_demandes/static/" + random_string + ".svg"
        # visualiser le graph du prediction
        make_picture(salaire_employe_,
                     _model,
                     scaler,
                     projet_form.region.data,
                     projet_form.profession.data,
                     projet_form.groupe.data,
                     projet_form.type_emploi.data,
                     float(pred),
                     int(projet_form.Annee.data),
                     path)

        # explain the feature importance
        # exp = explainer.explain_instance(final_df.to_numpy()[0], _model.predict, num_features=40)  # final_df.shape[1])
        # print(exp.as_list())
        global pred_as_str
        pred_as_str = "Salaire horaire moyen prédit :" + str(pred)

    return render_template('form_projet_input.html', title='Edition projet', form=projet_form,
                           output=pred_as_str, href=path[13:])


def make_picture(salaire_employe_, _model, scaler, region, cnp, grp_age, genr_emp, val_pred: float, val_annee_pred: int,
                 output_file):
    # visualisation

    sns.set_style('ticks')
    sns.set_context("notebook")
    sns.color_palette("hls", 8)
    x_train = salaire_employe_.drop(["Salaire horaire moyen"], axis=1)
    y_train = salaire_employe_["Salaire horaire moyen"]

    encoder_df = pd.DataFrame(
        scaler.transform(np.array(x_train[['Regions', 'CNP', 'Sexe', "Groupe d'âge", 'Genre de travail']]))).set_index(
        x_train.index)
    final_df = x_train.join(encoder_df)
    final_df.drop(columns=['Regions', 'CNP', 'Sexe', "Groupe d'âge", 'Genre de travail'], axis=1, inplace=True)

    prediction_train = _model.predict(final_df)
    # ------inverse operation de log--------------------------------------------

    prediction_train = np.round(np.exp(prediction_train), decimals=2)
    salaire_employe_["Prediction"] = prediction_train

    filtre_ = (salaire_employe_["Regions"] == region) & (salaire_employe_["CNP"] == cnp)
    # & (salaire_employe_["Groupe d'âge"] == grp_age) & (salaire_employe_["Genre de travail"] == genr_emp)

    fig = px.scatter(salaire_employe_[filtre_], x=salaire_employe_[filtre_]["Salaire horaire moyen"],
                     y=salaire_employe_[filtre_]["Prediction"],
                     trendline='ols',
                     # color='Sexe',
                     opacity=0.65,
                     labels={'x': 'le salaire horaire moyen réel', 'y': 'le salaire horaire moyen predit'}
                     )

    fig.add_trace(go.Scatter(x=[val_pred], y=[val_pred], mode='markers',
                             marker=dict(
                                 color='red',
                                 size=9,
                                 line=dict(
                                     color='MediumPurple',
                                     width=1
                                 )
                             ), ))

    fig.add_shape(
        type="line", line=dict(dash='dash'),

        x0=0, y0=0,
        x1=55, y1=55)
    fig.layout.update(title_text="Prediction taux salarial pour " + cnp,
                      font=dict(
                          family="Courier New, monospace",
                          size=9,
                          color="RebeccaPurple"
                      ),
                      xaxis_title='le salaire horaire moyen réel',
                      yaxis_title='le salaire horaire moyen predit',

                      xaxis_rangeslider_visible=True)

    fig.write_image(output_file, format='svg', engine='kaleido', height=350, width=650)
    salaire_employe_.drop(columns=['Prediction'], axis=1, inplace=True)
    fig.show()
