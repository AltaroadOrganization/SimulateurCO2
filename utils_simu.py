import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from csv import writer
from fpdf import FPDF
import math
import random
import datetime
import re
import boto3
import os
import base64
import warnings

warnings.filterwarnings("ignore")
plt.set_loglevel('WARNING')

#function to reload the state
@st.cache_data(show_spinner=False)
def download_state_management(_simulator_dict, ACCESS_KEY, SECRET_KEY):
    if 'download_done' not in st.session_state:
        st.session_state.download_done = True
    else:
        if st.session_state.download_done == False:
            bucket_name = 'dataset-altaroad-public'
            read_write_S3(bucket_name, _simulator_dict, ACCESS_KEY, SECRET_KEY)
        else:
            st.session_state.download_done=True

#function to check if an email is valid
def solve(s):
   pat = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

#function to give a random equivalent to a Carbon gain
def random_CO2_equivalent(Ea1):
    equivalent_CO2 = random.choice([str(math.ceil(Ea1 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea1 * 5181)) + " km en voiture (" + str(
                           math.ceil(Ea1 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea1)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea1 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea1 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea1 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea1 * 43)) + " jeans en coton 👖"])
    return equivalent_CO2

#function to load the dict to a S3 bucket
def read_write_S3(bucket_name, the_dict, access_key, secret_key):
    '''
    this function adds a "new simulator user file" to a bucket
    '''
    session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3 = session.resource('s3')
    heure=the_dict['date_heure'].replace('/','_').replace(' ','_')
    object = s3.Object(bucket_name, 'simulatorco2/simulatorUserfile_{}.txt'.format(heure))
    #df=pd.DataFrame.from_dict(the_dict)
    result = object.put(Body=str(the_dict))

#@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''<a href="{target_url}"><img src="data:image/{img_format};base64,{bin_str}" width="100%" height="auto"/></a>'''
    return html_code

#plot function
def pie_plot(inputs_list, labels_name, title, key_name):
    _fig, _ax = plt.subplots(figsize=(8,8))
    _ax.set_title("Distribution {}".format(key_name), color="#F05E16", size=20)
    _ax.pie(inputs_list, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=False,
            colors=["#264653","#2A9D8F","#E9C46A","#F4A261","#E76F51"])
    _ax.axis('equal')
    legend = _ax.legend(labels_name, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor="black",
                        edgecolor="#F4A261")
    legend.set_title(title)
    title = legend.get_title()
    title.set_color("#F4A261")
    title.set_size(18)
    plt.savefig('./figures/pie_plot_Distribution {}.jpg'.format(key_name),bbox_inches='tight')
    return _fig

def bar_plot(inputs_list, labels_name, title, x_label_title, y_label_title):
    _fig = plt.figure(figsize=(8,8))
    _ax = _fig.add_axes([0, 0, 1, 1])
    _ax.set_title(title, color="#F4A261", size=20)
    _ax.set_ylabel(y_label_title, color="#67686b", size=14)
    _ax.set_xlabel(x_label_title, color="#67686b", size=14)
    plt.xticks(rotation=45)
    _ax.bar(labels_name, inputs_list, color="#2A9D8F", edgecolor="#264653")
    plt.savefig('./figures/bar_plot_{}.jpg'.format(title), bbox_inches='tight')
    return _fig

#get data function
@st.cache_data(show_spinner=False)
def get_dataBase_func():
    bdd_d = "Base_Carbone_FE_S3.csv"
    BDD_FE_S3 = pd.read_csv(bdd_d, encoding="latin1", sep=";", decimal=',')
    bdd_s2 = "Base_Carbone_FE_S1et2.csv"
    BDD_FE_S2 = pd.read_csv(bdd_s2, encoding="latin1", sep=";", decimal=',')
    bdd_ouv = "data_FE_ouvrages.csv"
    BDD_FE_OUV = pd.read_csv(bdd_ouv, encoding="latin1", sep=";", decimal=',')
    return BDD_FE_S3, BDD_FE_S2, BDD_FE_OUV

#function to create the pdf report
def build_pdf_from_dict(the_input_dict):
    pdf = FPDF()
    pdf.add_font('sen', '', 'sen.ttf', uni=True)
    pdf.add_page()
    pdf.image('Banner_Linkedin.png',w=190)
    pdf.set_font("sen", "", size=2)
    pdf.set_margins(10,10,10)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.image('logo.png',w=50,x=10)
    pdf.set_font("sen", "", size=2)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=24)
    pdf.set_text_color(243, 113, 33)
    pdf.cell(200, 10, txt="Simulateur CO2 du chantier", ln=1, align='C')
    pdf.set_text_color(128, 128, 128)
    pdf.set_font("sen", "", size=16)
    pdf.cell(200, 10, txt="Synthèse des résultats", ln=1, align='C')
    pdf.set_font("sen", size=8, style='')
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Document généré automatiquement par ALTAROAD le "+the_input_dict["date_heure"], ln=1)
    pdf.cell(200, 2, txt="", ln=2)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="LE CHANTIER simulé", ln=1)
    pdf.set_font("sen", size=10)
    pdf.set_text_color(0, 0, 0)
    str_text1="Ce document résume l'estimation des émissions de GES (exprimées en CO2e), du chantier " \
              + the_input_dict["type_chantier"] + " opéré pour la construction de " \
              + the_input_dict["categorie_ouvrage"]+" de dimensions de " + str(the_input_dict["DO_ouv"]) + " " \
              + the_input_dict["u"] + " situé à : " + the_input_dict["lieu_chantier"]+" et d'une durée de " \
              + str(the_input_dict["duree_semaine_chantier"]) + " semaines"
    pdf.write(4, txt=str_text1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.cell(200, 4, txt="", ln=1)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 1&2 : Consommations d'énergies", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("sen", "", size=10)
    pdf.cell(200, 4, txt="Estimations du bilan CO2e des Scopes 1 & 2: " + str(the_input_dict["tot_S1et2"]) + " tCO2e", ln=1)
    pdf.set_font("sen", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Scope 1 : " + str(the_input_dict["tot_S1"]) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Scope 2 : " + str(the_input_dict["tot_S2"]) + " tCO2e", ln=1)
    pdf.cell(200, 4, txt="", ln=1)
    pdf.set_text_color(128, 128, 128)
    pdf.set_font("sen", "", size=16)
    pdf.cell(200, 10, txt="SCOPE 3 : Evacuation des déchets", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Données d'entrée", ln=1)
    pdf.set_font("sen", size=10)
    pdf.cell(10)
    if the_input_dict["ISDI1"]>0 :
        pdf.cell(200, 4, txt="- Terres : " + str(the_input_dict["ISDI1"]) + " tonnes, chantier > centre de collecte : " + str(the_input_dict["dist_exuISDI1"]) + " km",ln=1)
        pdf.cell(10)
    if the_input_dict["ISDI2"]>0:
        pdf.cell(200, 4, txt="- Gravats : " + str(the_input_dict["ISDI2"]) + " tonnes, chantier > centre de collecte : " + str(the_input_dict["dist_exuISDI2"]) + " km",
             ln=1)
        pdf.cell(10)
    if the_input_dict["ISDND"]>0:
        pdf.cell(200, 4, txt="- Déchets non-dangereux : " + str(the_input_dict["ISDND"]) + " tonnes, chantier > centre de collecte : " + str(
            the_input_dict["dist_exuISDND"]) + " km", ln=1)
        pdf.cell(10)
    if the_input_dict["ISDD"]>0:
        pdf.cell(200, 4,
                 txt="- Déchets dangereux : " + str(the_input_dict["ISDD"]) + " tonnes, chantier > centre de collecte : " + str(the_input_dict["dist_exuISDD"]) + " km",
                 ln=1)
        pdf.cell(10)
    pdf.cell(200, 4, txt="- Nombre de passages quotidien : " + str(the_input_dict["pass_jour"]), ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Taux de réemploi des terres/gravats : " + str(the_input_dict["repl_terres"]) + "%", ln=1)
    pdf.cell(10)
    if the_input_dict["nb_cam5"]>0:
        pdf.cell(200, 4, txt="- Camions 5 essieux articulés : " + str(the_input_dict["nb_cam5"]) + " soit " + str(int(the_input_dict["cam5"])) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Chargement moyen des 5 essieux : " + str(the_input_dict["load_cam5"]) + "t" , ln=1)
        pdf.cell(10)
    if the_input_dict["nb_cam4"]>0:
        pdf.cell(200, 4, txt="- Camions 4 essieux porteurs : " + str(the_input_dict["nb_cam4"]) + " soit " + str(int(the_input_dict["cam4"])) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Chargement moyen des 4 essieux : " + str(the_input_dict["load_cam4"])+"t", ln=1)
        pdf.cell(10)
    if the_input_dict["nb_cam2"]>0:
        pdf.cell(200, 4, txt="- Camions 2 essieux porteurs : " + str(the_input_dict["nb_cam2"]) + " soit " + str(int(the_input_dict["cam2"])) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Chargement moyen des 2 essieux : " + str(the_input_dict["load_cam2"])+"t", ln=1)
        pdf.cell(10)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=10)
    pdf.cell(200, 4, txt="Données de sortie", ln=1)
    pdf.set_font("sen", size=10)
    str_text2= "La partie évacuation est évaluée à " + str(round(the_input_dict["dist_tot"],1)) + " km, effectuée en "+ str(int(the_input_dict["pass_tot"])) + " passages et " + str(round(the_input_dict["jours_evacuation"],1)) + " jours."
    pdf.write(4, txt=str_text2)
    pdf.set_font("sen", "", size=10)
    pdf.cell(200, 10, txt="", ln=1)
    pdf.cell(200, 4, txt="Bilan CO2e pour le SCOPE3 évacuation: " + str(round(the_input_dict["E_tot"],1)) + " tCO2e", ln=1)
    pdf.set_font("sen", size=10)
    if the_input_dict["E_tot"] > 0:
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Emissions CO2e totales 'Transport' : " + str(round(the_input_dict["E_trans"],1)) + " tCO2e, soit " + str(
            int((the_input_dict["E_trans"] / the_input_dict["E_tot"]) * 100)) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Emissions CO2e totales 'Valorisation' : " + str(round(the_input_dict["E_valo"],1)) + " tCO2e, soit " + str(
            int((the_input_dict["E_valo"] / the_input_dict["E_tot"]) * 100)) + " %", ln=1)
        pdf.set_font("sen", "", size=10)
        pdf.cell(200, 4, txt="", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'Terres' : "  +str(round(the_input_dict["E_ISDI1"] + the_input_dict["E_trans_ISDI1"],1)) + " tCO2e (Transport = " + str(
        round(the_input_dict["E_trans_ISDI1"],1)) + " tCO2e; Valorisation = " + str(round(the_input_dict["E_ISDI1"],1)) + " tCO2e)", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'Gravats' : "+str(round(the_input_dict["E_ISDI2"] + the_input_dict["E_trans_ISDI2"],1)) + " tCO2e (Transport = " + str(
        round(the_input_dict["E_trans_ISDI2"],1)) + " tCO2e; Valorisation = " + str(round(the_input_dict["E_ISDI2"],1)) + " tCO2e)", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="- Emissions CO2e 'DND' : " + str(round(the_input_dict["E_ISDND"] + the_input_dict["E_trans_ISDND"],1)) + " tCO2e (Transport = " + str(round(the_input_dict["E_trans_ISDND"],1)) + " tCO2e; Valorisation = " + str(
                 round(the_input_dict["E_ISDND"],1)) + " tCO2e)", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="- Emissions CO2e 'DD' : " + str(round(the_input_dict["E_ISDD"] + the_input_dict["E_trans_ISDD"],1)) + " tCO2e (Transport = " + str(round(the_input_dict["E_trans_ISDD"],1)) + " tCO2e; Valorisation = " + str(
                 round(the_input_dict["E_ISDD"],1)) + " tCO2e)", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=10)
    pdf.cell(200, 4, txt="Actions de réduction et gains", ln=1)
    pdf.set_font("sen", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="Choix d'une flotte de véhicules économe : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(round(the_input_dict["Ea1"],1)) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_ISDI1"] - the_input_dict["new_pass_ISDI1"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea1"] + the_input_dict["eco_ISDI"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="Optimisation du chargement des camions (+2T) : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(round(the_input_dict["Ea2"],1)) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea2"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea2"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea2"] + the_input_dict["eco_D_tot_Ea2"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="+10% de taux de valorisation des déchets : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(round(the_input_dict["Ea3"],1)) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea3"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea3"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea3"] + the_input_dict["eco_D_tot_Ea3"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="-10 km de distance au centre de collecte : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4,txt="- Gain CO2e = " + str(round(the_input_dict["Ea4"],1)) + " tCO2e;",ln=1)
    pdf.cell(20)
    pdf.cell(200, 4,txt="- Gain économique = " + str(math.ceil(the_input_dict["eco_c_Ea4"])) + " euros",ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="Toutes les actions de réductions combinées : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(round(the_input_dict["Ea5"],1)) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea5"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea5"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea5"] + the_input_dict["eco_D_tot_Ea5"])) + " euros", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 3 : Autres déchets & achats Matériaux", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'autres déchets' : " + str(the_input_dict["tot_S3d"]) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'achats Matériaux' : " + str(the_input_dict["tot_S3a"]) + " tCO2e", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 3 : Construction de l'ouvrage ", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", size=10)
    pdf.set_text_color(0, 0, 0)
    str_text3="Selon les données de l'ADEME, la construction de ce type d'ouvrage d'une surface de " + str(
        int(the_input_dict["DO_ouv"])) + " m2, émettrait environ " + str(round(the_input_dict["EMISSIONS_ouv"],1)) + " tCO2e (+ ou - " + str(
                 int(the_input_dict["INCERTITUDE_ouv"])) + " tonnes CO2e)."
    pdf.write(4, txt=str_text3)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.cell(200, 4, txt="", ln=1)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="Estimation du bilan CO2e total", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("sen", '', size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Total des émissions CO2e : " + str(
        round(the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"] + the_input_dict["tot_S1et2"],1)) + " tCO2e",
             ln=1)
    pdf.set_font("sen", '', size=10)
    if the_input_dict["E_tot"] > 0:
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Scope 1 : " + str(round(the_input_dict["tot_S1"], 1)) + " tCO2e, soit " + str(
            round((the_input_dict["tot_S1"] / (the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"] + the_input_dict["tot_S1et2"])) * 100, 1)) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4, txt="- Scope 2 : " + str(round(the_input_dict["tot_S2"], 1)) + " tCO2e, soit " + str(
            round((the_input_dict["tot_S2"] / (the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"] + the_input_dict["tot_S1et2"])) * 100, 1)) + " %", ln=1)
        pdf.cell(10)
        pdf.cell(200, 4,
                 txt="- Scope 3 : " + str(round(the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"], 1)) + " tCO2e, soit " + str(
                     round(((the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"]) / (
                                 the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"] + the_input_dict["tot_S1et2"])) * 100, 1)) + " %", ln=1)
    else:
        pdf.cell(200, 10, txt="Aucune donnée saisie", ln=1)

    #ajout des figures
    pdf.add_page()
    pdf.cell(200, 10, txt="", ln=1)
    pdf.set_font("sen", "", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="FIGURES", ln=1)
    directory = './figures'
    i=1
    y_fig=pdf.y
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.jpg'):
                if i % 2 != 0:
                    y_fig=pdf.y
                    pdf.image('./figures/{}'.format(filename), w=50)
                if i % 2 == 0:
                    pdf.image('./figures/{}'.format(filename), w=50, x=110, y=y_fig)
                i+=1

    pdf.add_page()
    pdf.set_font("sen", size=8, style='')
    pdf.set_text_color(128, 128, 128)
    str_textEnd="Ce simulateur propose une estimation des émissions CO2e d'un chantier. Il s'agit d'un outil dont l'objectif" \
                " est d'anticiper les émissions CO2e pour les éviter. Les calculs sont basés sur des données sources fiables mais " \
                "les résultats ne doivent pas être interprétés comme un Bilan Énergétique des Gaz à Effet de Serre (BEGES) certifié dont " \
                "la méthodologie est définie par l'ADEME et ne peut être délivré que par des experts accrédités. Il convient à l'utilisateur " \
                "de renseigner les données les plus fiables possibles afin de réduire les incertitudes des résultats obtenus."
    pdf.write(4, txt=str_textEnd)
    pdf.cell(200, 20, txt="", ln=1)
    pdf.image('Banner_Linkedin.png',w=190)
    pdf = pdf.output("ALTAROAD_Simulateur_CO2_SYNTHESE.pdf")
    return st.write("le rapport a été généré")