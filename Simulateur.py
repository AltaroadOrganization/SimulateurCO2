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

#get AWS access key and secret key
ACCESS_KEY = st.secrets["my_access_key"]["ACCESS_KEY"]
SECRET_KEY = st.secrets["my_access_key"]["SECRET_KEY"]

#function to check if an email is valid
def solve(s):
   pat = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

#function to give a random equivalent to a Carbon gain
def random_CO2_equivalent(Ea1):
    v = random.choice([str(math.ceil(Ea1 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea1 * 5181)) + " km en voiture (" + str(
                           math.ceil(Ea1 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea1)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea1 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea1 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea1 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea1 * 43)) + " jeans en coton 👖"])
    return v

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

#function to create the pdf report
def build_pdf_from_dict(the_input_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.image('Banner_Linkedin.png',w=190)
    pdf.set_font("Arial", "B", size=2)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.image('logo.png',w=50,x=10)
    pdf.set_font("Arial", "B", size=2)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=24)
    pdf.set_text_color(243, 113, 33)
    pdf.cell(200, 10, txt="Simulateur CO2 du chantier", ln=1, align='C')
    pdf.set_text_color(128, 128, 128)
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200, 10, txt="Synthèse des résultats", ln=1, align='C')
    pdf.set_font("Arial", size=8, style='I')
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Document généré automatiquement par ALTAROAD le "+the_input_dict["date_heure"], ln=1)
    pdf.cell(200, 2, txt="", ln=2)
    pdf.set_font("Arial", "B", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="LE CHANTIER simulé", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Ce document résume l'estimation des émissions CO2", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Du chantier : " + the_input_dict["type_chantier"],ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Pour la construction de : " + the_input_dict["categorie_ouvrage"],ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Situé à : " + the_input_dict["lieu_chantier"], ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- De taille : " + the_input_dict["taille_chantier"], ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- D'une duréee de " + the_input_dict["duree_semaine_chantier"] + ' semaines', ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 1&2 : Consommations d'énergies", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(200, 4, txt="Estimations du bilan CO2 des Scopes 1 & 2", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Scope 1 : " + str(the_input_dict["tot_S1"]) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Scope 2 : " + str(the_input_dict["tot_S2"]) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Scopes 1 & 2 : " + str(the_input_dict["tot_S1et2"]) + " tCO2e", ln=1)
    pdf.cell(200, 4, txt="", ln=1)
    pdf.set_text_color(128, 128, 128)
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200, 10, txt="SCOPE 3 : Evacuation des déchets", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Données d'entrée", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Terres : " + str(the_input_dict["ISDI1"]) + " tonnes, chantier > exutoire : " + str(the_input_dict["dist_exuISDI1"]) + " km",
             ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Gravats : " + str(the_input_dict["ISDI2"]) + " tonnes, chantier > exutoire : " + str(the_input_dict["dist_exuISDI2"]) + " km",
             ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Déchets non-dangereux : " + str(the_input_dict["ISDND"]) + " tonnes, chantier > exutoire : " + str(
        the_input_dict["dist_exuISDND"]) + " km", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="- Déchets dangereux : " + str(the_input_dict["ISDD"]) + " tonnes, chantier > exutoire : " + str(the_input_dict["dist_exuISDD"]) + " km",
             ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Nombre de passages quotidien : " + str(the_input_dict["pass_jour"]), ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Taux de réemploi des terres : " + str(the_input_dict["repl_terres"]) + "%", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Camions 5 essieux articulés : " + str(the_input_dict["nb_cam5"]) + " soit " + str(int(the_input_dict["cam5"])) + " %", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Chargement moyen des 5 essieux : " + str(the_input_dict["load_cam5"]) + "T" , ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Camions 4 essieux porteurs : " + str(the_input_dict["nb_cam4"]) + " soit " + str(int(the_input_dict["cam4"])) + " %", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Chargement moyen des 4 essieux : " + str(the_input_dict["load_cam4"])+"T", ln=1)
    pdf.cell(10)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(200, 4, txt="Données de sortie", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Distance totale à parcourir : " + str(int(the_input_dict["dist_tot"])) + " km", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Nombre total de passages : " + str(int(the_input_dict["pass_tot"])), ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Nombre de jours d'évacuation : " + str(int(the_input_dict["jours_evacuation"])), ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.cell(200, 4, txt="Bilan CO2e", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e totales estimées : " + str(int(the_input_dict["E_tot"])) + " tCO2e", ln=1)
    if the_input_dict["E_tot"] > 0:
        pdf.cell(20)
        pdf.cell(200, 4, txt="- Emissions CO2e totales 'Transport' : " + str(int(the_input_dict["E_trans"])) + " tCO2e, soit " + str(
            int((the_input_dict["E_trans"] / the_input_dict["E_tot"]) * 100)) + " %", ln=1)
        pdf.cell(20)
        pdf.cell(200, 4, txt="- Emissions CO2e totales 'Valorisation' : " + str(int(the_input_dict["E_valo"])) + " tCO2e, soit " + str(
            int((the_input_dict["E_valo"] / the_input_dict["E_tot"]) * 100)) + " %", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'Terres' : "  "Transport = " + str(
        int(the_input_dict["E_trans_ISDI1"])) + " tCO2e; Valorisation = " + str(int(the_input_dict["E_ISDI1"])) + " tCO2e; Total = " + str(
        int(the_input_dict["E_ISDI1"] + the_input_dict["E_trans_ISDI1"])) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions CO2e 'Gravats' : "  "Transport = " + str(
        int(the_input_dict["E_trans_ISDI2"])) + " tCO2e; Valorisation = " + str(int(the_input_dict["E_ISDI2"])) + " tCO2e; Total = " + str(
        int(the_input_dict["E_ISDI2"] + the_input_dict["E_trans_ISDI2"])) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="- Emissions CO2e 'DND' : "  "Transport = " + str(int(the_input_dict["E_trans_ISDND"])) + " tCO2e; Valorisation = " + str(
                 int(the_input_dict["E_ISDND"])) + " tCO2e; Total = " + str(int(the_input_dict["E_ISDND"] + the_input_dict["E_trans_ISDND"])) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="- Emissions CO2e 'DD' : "  "Transport = " + str(int(the_input_dict["E_trans_ISDD"])) + " tCO2e; Valorisation = " + str(
                 int(the_input_dict["E_ISDD"])) + " tCO2e; Total = " + str(int(the_input_dict["E_ISDD"] + the_input_dict["E_trans_ISDD"])) + " tCO2e", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(200, 4, txt="Actions de réduction et gains", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="+ 10% de réutilisation des terres sur site : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(int(the_input_dict["Ea1"])) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_ISDI1"] - the_input_dict["new_pass_ISDI1"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea1"] + the_input_dict["eco_ISDI"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="+ 15% de camions 5 essieux articulés : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(int(the_input_dict["Ea2"])) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea2"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea2"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea2"] + the_input_dict["eco_D_tot_Ea2"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="+ 2 tonnes de chargement moyen en + : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(int(the_input_dict["Ea3"])) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea3"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea3"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea3"] + the_input_dict["eco_D_tot_Ea3"])) + " euros", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- 10 km de distance à l'exutoire : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4,txt="- Gain CO2e = " + str(int(the_input_dict["Ea4"])) + " tCO2e;",ln=1)
    pdf.cell(20)
    pdf.cell(200, 4,txt="- Gain économique = " + str(math.ceil(the_input_dict["eco_c_Ea4"])) + " euros",ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="Toutes les actions de réductions combinées : ", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain CO2e = " + str(int(the_input_dict["Ea5"])) + " tCO2e;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain passages = " + str(
        int(the_input_dict["pass_tot"] - the_input_dict["new_pass_tot_Ea5"])) + " soit " + str(
        math.ceil(the_input_dict["jours_evacuation"] - (the_input_dict["new_pass_tot_Ea5"] / the_input_dict["pass_jour"]))) + " jours;", ln=1)
    pdf.cell(20)
    pdf.cell(200, 4, txt="- Gain économique = " + str(
        math.ceil(the_input_dict["eco_c_Ea5"] + the_input_dict["eco_D_tot_Ea5"])) + " euros", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 3 : Autres déchets & achats", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Estimations CO2 autres déchets et achats", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions GES 'autres déchets' : " + str(the_input_dict["tot_S3d"]) + " tCO2e", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4, txt="- Emissions GES 'achats' : " + str(the_input_dict["tot_S3a"]) + " tCO2e", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="SCOPE 3 : Construction de l'ouvrage", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Estimations du bilan CO2 de la construction de l'ouvrage", ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(10)
    pdf.cell(200, 4, txt="Selon les données de l'ADEME, la construction de ce type d'ouvrage d'une surface de " + str(
        int(the_input_dict["DO_ouv"])) + " m²,", ln=1)
    pdf.cell(10)
    pdf.cell(200, 4,
             txt="émettrait environ " + str(int(the_input_dict["EMISSIONS_ouv"])) + " tCO2e (+ ou - " + str(
                 int(the_input_dict["INCERTITUDE_ouv"])) + " tCO2e).",
             ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", "B", size=16)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 10, txt="Estimation du bilan CO2 total", ln=1)
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", 'B', size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 4, txt="Total des émissions GES : " + str(
        int(the_input_dict["E_tot"] + the_input_dict["EMISSIONS_ouv"] + the_input_dict["tot_S3d"] + the_input_dict["tot_S3a"] + the_input_dict["tot_S1et2"])) + " tCO2e",
             ln=1)
    pdf.set_font("Arial", size=10)
    if E_tot > 0:
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
    pdf.cell(200, 2, txt="", ln=1)
    pdf.set_font("Arial", size=8, style='I')
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 4, txt="Ce simulateur propose une estimation des émissions CO2 d'un chantier. Il s'agit d'un outil dont l'objectif", ln=1)
    pdf.cell(200, 4, txt="est d'anticiper les émissions CO2 pour les éviter. Les calculs sont basés sur des données sources fiables", ln=1)
    pdf.cell(200, 4, txt="mais les résultats ne doivent pas être interprétés comme un Bilan Énergétique des Gaz à Effet de Serre (BEGES) certifié", ln=1)
    pdf.cell(200, 4, txt="dont la méthodologie est définie par l'ADEME et ne peut être délivré que par des experts accrédités. Il convient à l'utilisateur de renseigner ", ln=1)
    pdf.cell(200, 4, txt="les données les plus fiables possibles afin de réduire les incertitudes des résultats obtenus.", ln=1)
    pdf = pdf.output("ALTAROAD_Simulateur_CO2_SYNTHESE.pdf")
    return st.write("le rapport a été généré")

#all the inputs and outputs are saved in a dict
simulator_dict={}

Image_title=Image.open("Banner_Linkedin.png")
st.image(Image_title)

col1, col2 = st.columns([1, 1])
image = Image.open("logo.png")
now = datetime.datetime.utcnow()
result = now + datetime.timedelta(hours=2)
date_heure = result.strftime("%d/%m/%Y %H:%M:%S")
date = result.strftime("%d/%m/%Y")
heure = result.strftime("%H:%M:%S")
st.text("Date et heure : {}".format(date_heure))
simulator_dict['date_heure']=date_heure

with col1:
    original_title = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; letter-spacing: -1px; line-height: 1.2; font-size: 40px;">Simulateur CO2 du chantier</p>
    </head>
    '''
    st.markdown(original_title, unsafe_allow_html=True)
with col2:
    st.image(image)

FEterres = 4.58
FEgravats = 12
FEdnd = 84
FEdd = 128
FEmoy5e = 0.0711 / 1000
FEmoy4e = 0.105 / 1000
mav5e = 15
mav4e = 12
prix_c = 2
prix_ISDI1 = 300
prix_ISDI2 = 300
prix_ISDND = 1500
prix_ISDD = 5000
conso_moy = 30 / 100
st.write("")
st.write("Cet outil permet de simuler les émissions carbone de votre chantier en intégrant tous les SCOPES avec les quantités d'énergie, de déchets et de matériaux nécessaires à l'ouvrage.")
st.write("")

st.write("Pour plus d'information, téléchargez le Manifeste ici")
with open('LeManifeste_SimulateurCO2_Altaroad.pdf', "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="le Manifeste",
                   data=PDFbyte,
                   file_name="LeManifeste_SimulateurCO2_Altaroad.pdf",
                   mime='application/octet-stream')

header0 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Les infos du chantier</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header0, unsafe_allow_html=True)
st.write('Ici, vous entrez quelques infos sur le chantier que vous souhaitez simuler')
type_chantier = st.selectbox("Type de chantier :", ['CONSTRUCTION','DEMOLITION','TERRASSEMENT'])
lieu_chantier = st.text_input('le lieu du chantier (entrer une adresse)', value="", max_chars=None, key=None, type="default")
col1,col2=st.columns(2)
taille_chantier = col1.selectbox('la taille du chantier', ['PETIT','MOYEN','GROS'])
duree_semaine_chantier=col2.text_input('durée en  semaines', value="", max_chars=None, key=None, type="default")

simulator_dict['type_chantier']=type_chantier
simulator_dict['lieu_chantier']=lieu_chantier
simulator_dict['taille_chantier']=taille_chantier
simulator_dict['duree_semaine_chantier']=duree_semaine_chantier

header1 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPES 1&2 : Consommations d'énergies 🔋</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header1, unsafe_allow_html=True)
#st.header("SCOPE 1&2 : Consommations d'énergies 🔋")
st.write("Ici, vous pouvez simuler les émissions carbone directes et indirectes des Scopes 1 & 2 liées aux consommations d'énergies fossiles et d'électricité")
st.write("Cliquer sur Rafraîchir avant de démarrer 🔄")
if st.button('Rafraîchir Scope 1 et 2'):
    scope2 = "scope2_blank.csv"
    df_S2 = pd.read_csv(scope2, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S2[df_S2.columns]=""
    df_S2.to_csv('scope2_blank.csv')
    scope1 = "scope1_blank.csv"
    df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S1[df_S1.columns]=""
    df_S1.to_csv('scope1_blank.csv')

with st.expander("Scope1 - Energies fossiles 🛢️"):
    scope1 = "scope1_blank.csv"
    df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S1=df_S1.dropna()
    bdd_s2 = "Base_Carbone_FE_S1et2.csv"
    df = pd.read_csv(bdd_s2, encoding="latin1", sep=";", decimal=',')
    df["Sous catégorie 1"] = df["Sous catégorie 1"].astype(str)
    df["Sous catégorie 2"] = df["Sous catégorie 2"].astype(str)
    df["Sous catégorie 3"] = df["Sous catégorie 3"].astype(str)
    df["Sous catégorie 4"] = df["Sous catégorie 4"].astype(str)
    df["Nom attribut français"] = df["Nom attribut français"].astype(str)
    df["Unité français"] = df["Unité français"].astype(str)
    df = df[df['Code de la catégorie'].str.contains(str("Combustibles "))]
    df = df[df['Sous catégorie 1'].str.contains(str(" Fossiles "))]
    type = st.radio("Type d'énergie", ('Liquide', 'Gaz'))
    if type == 'Liquide':
        df = df[df['Sous catégorie 2'].str.contains(str(" Liquides "))]
    elif type == 'Gaz':
        df = df[df['Sous catégorie 2'].str.contains(str(" Gazeux "))]
    df = df[df['Sous catégorie 4'] == " Usage routier ou non-routier"]
    choix_fe = st.selectbox("Choix du facteur d'émissions :", df["Nom base français"].unique())
    df = df[df['Nom base français'] == choix_fe]
    choix_attribut = st.selectbox("Choix de l'attribut :", df['Nom attribut français'].unique())
    df = df[df["Nom attribut français"] == choix_attribut]
    choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
    df = df[df["Unité français"] == choix_unite]
    for u in df["Unité français"]:
        u = u[7:].lower()
    DO = float(st.number_input("Quantité estimée (en " + u + ") : ", step=1))
    for x in df["Total poste non décomposé"]:
        x = float(x)
    for i in df["Incertitude"]:
        i = float(i)
    EMISSIONS = round(x / 1000 * DO, 2)
    INCERTITUDE = round(EMISSIONS * 0.01 * i, 2)
    POSTE = str(df['Nom base français'].unique())
    ATT = str(df['Nom attribut français'].unique())
    st.write(" ")
    st.write(" ")
    st.text(
        "Emissions GES de la donnée 💨 : " + str(EMISSIONS) + " tCO2e " + "(+ ou - " + str(INCERTITUDE) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕"):
        new = ["Scope1",POSTE, ATT, str(DO), u, EMISSIONS]
        with open(scope1, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()

with st.expander("Scope2 - Electricité ⚡"):
    scope2 = "scope2_blank.csv"
    elec_moy = 0.0569
    i2 = 10
    u2 = "kWh"
    DO2 = float(st.number_input("Quantité estimée (en " + u2 + ") : ", step=1))
    EMISSIONS2 = round(elec_moy / 1000 * DO2, 2)
    INCERTITUDE2 = round(EMISSIONS2 * 0.01 * i2, 2)
    POSTE2 = "['Electricité']"
    st.write(" ")
    st.write(" ")
    st.text("Emissions GES de la donnée 💨 : " + str(EMISSIONS2) + " tCO2e " + "(+ ou - " + str(
        INCERTITUDE2) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕  "):
        new2 = ["Scope2",POSTE2, "-", str(DO2), u2, EMISSIONS2]
        with open(scope2, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new2)
            f_object.close()

with st.expander("Résultats 📊"):
    df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S1 = df_S1.dropna()
    df_S2 = pd.read_csv(scope2, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S2 = df_S2.dropna()
    df_S1et2 = pd.concat([df_S1, df_S2])
    st.dataframe(df_S1et2)
    tot_S1 = round(df_S1["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES du scope 1 🛢️ 🌍 : " + str(tot_S1) + " tCO2e")
    tot_S2 = round(df_S2["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES du scope 2 ⚡ 🌍 : " + str(tot_S2) + " tCO2e")
    tot_S1et2 = round(df_S1et2["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES des scopes 1 & 2 🛢️+⚡ 🌍 : " + str(tot_S1et2) + " tCO2e")
    st.write(" ")

    col1, col2 = st.columns(2)
    with col1:
        if tot_S1 > 0 or tot_S2 > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_S1et2["Donnee"]
            es = df_S1et2["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES des Scopes 1 et 2', color = "#f37121", fontfamily = 'sen', size = 28 )
            ax.set_ylabel('Emissions (tCO2e)', color =  "#67686b", fontfamily = 'sen', size = 18)
            ax.set_xlabel('Données', color =  "#67686b", fontfamily = 'sen', size = 18 )
            plt.xticks(rotation=45)
            ax.bar(poste, es, color="#f37121", edgecolor="#67686b", linewidth=4)
            st.pyplot(fig)
    with col2:
        if tot_S1 > 0 or tot_S2 > 0:
            labels = '1', '2'
            sizes = [tot_S1, tot_S2]
            fig1, ax1 = plt.subplots()
            ax1.set_title("Part des émissions GES par scope", color = "#f37121", fontfamily = 'sen', size = 28)
            ax1.pie(sizes, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b"])
            ax1.axis('equal')
            legend = ax1.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Scope")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig1)


simulator_dict['tot_S1']=tot_S1
simulator_dict['tot_S2']=tot_S2
simulator_dict['tot_S1et2']=tot_S1et2

header2 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Evacuation des déchets 🗑️</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header2, unsafe_allow_html=True)
#st.header('SCOPE 3 : Evacuation des déchets 🗑️')
st.write('Ici, vous simulez les évacuations des déchets, et leur traitement')
col1, col2 = st.columns(2)
with col1:
    subheader1 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Quantité de déchets à évacuer 🚮</p>
    </head>
    '''
    st.markdown(subheader1, unsafe_allow_html=True)
    #st.subheader("Quantité de déchets à évacuer 🚮")
    ISDI1brut = st.number_input("Terres à excaver (en tonnes)", step=1)
    ISDI2 = st.number_input("Déchets inertes : Gravats (en tonnes)", step=1)
    ISDND = st.number_input("Déchets non-dangereux en mélange (en tonnes)", step=1)
    ISDD = st.number_input("Déchets dangereux (en tonnes)", step=1)
    simulator_dict['ISDI1brut'] = ISDI1brut
    simulator_dict['ISDI2'] = ISDI2
    simulator_dict['ISDND'] = ISDND
    simulator_dict['ISDD'] = ISDD


with col2:
    subheader2 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Distance chantier-exutoire ↔</p>
    </head>
    '''
    st.markdown(subheader2, unsafe_allow_html=True)
    #st.subheader("Distance chantier-exutoire ↔")
    dist_exuISDI1 = st.number_input("Distance exutoire 1 (en km)", value=35, step=1)
    dist_exuISDI2 = st.number_input("Distance exutoire 2 (en km)", value=35, step=1)
    dist_exuISDND = st.number_input("Distance exutoire 3 (en km)", value=35, step=1)
    dist_exuISDD = st.number_input("Distance exutoire 4 (en km)", value=35, step=1)
    simulator_dict['dist_exuISDI1'] = dist_exuISDI1
    simulator_dict['dist_exuISDI2'] = dist_exuISDI2
    simulator_dict['dist_exuISDND'] = dist_exuISDND
    simulator_dict['dist_exuISDD'] = dist_exuISDD

col1, col2 = st.columns(2)
with col1:
    subheader3 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Nombre de passages quotidiens 🔃</p>
    </head>
    '''
    st.markdown(subheader3, unsafe_allow_html=True)
    #st.subheader("Nombre de passages quotidiens 🔃")
    pass_jour = st.slider("Nombre de passages quotidien estimés", 10, 100, 50, step=5)
    simulator_dict['pass_jour'] = pass_jour

with col2:
    subheader4 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Taux de réemploi des terres ♻</p>
    </head>
    '''
    st.markdown(subheader4, unsafe_allow_html=True)
    #st.subheader("Taux de réemploi des terres ♻️")
    repl_terres = st.slider("Réemploi des terres sur site (%)", 0, 100, 0, step=5)
    valo_terres = 100 - repl_terres
    ISDI1 = math.ceil(ISDI1brut * (valo_terres / 100))
    simulator_dict['repl_terres'] = repl_terres
    simulator_dict['ISDI1'] = ISDI1

col1, col2 = st.columns(2)
with col1:
    subheader5 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Types de camions 🚛</p>
    </head>
    '''
    st.markdown(subheader5, unsafe_allow_html=True)
    #st.subheader("Types de camions 🚛")
    nb_cam5 = st.number_input("Nombre de camions 5 essieux articulés", value=20, step=1)
    nb_cam4 = st.number_input("Nombre de camions 4 essieux porteurs", value=10, step=1)
    cam5 = (nb_cam5 / (nb_cam5 + nb_cam4)) * 100
    cam4 = (nb_cam4 / (nb_cam5 + nb_cam4)) * 100
    simulator_dict['nb_cam5'] = nb_cam5
    simulator_dict['nb_cam4'] = nb_cam4
    simulator_dict['cam5'] = cam5
    simulator_dict['cam4'] = cam4

with col2:
    subheader6 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Chargements 🚚</p>
    </head>
    '''
    st.markdown(subheader6, unsafe_allow_html=True)
    #st.subheader("Chargements 🚚")
    load_cam5 = st.slider("Chargement moyen des camions articulés (tonnes)", 15, 29, 25, step=1)
    load_cam4 = st.slider("Chargement moyen des camions porteurs (tonnes)", 10, 20, 15, step=1)
    simulator_dict['load_cam5'] = load_cam5
    simulator_dict['load_cam4'] = load_cam4

pass_ISDI1 = math.ceil(ISDI1 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDI2 = math.ceil(ISDI2 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDND = math.ceil(ISDND / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDD = math.ceil(ISDD / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_tot = pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
FE_trans = FEmoy5e * (cam5 / 100) + FEmoy4e * (cam4 / 100)
tot_D = ISDI1 + ISDI2 + ISDND + ISDD
dist_tot = pass_ISDI1 * dist_exuISDI1 + pass_ISDI2 * dist_exuISDI2 + pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD
simulator_dict['pass_ISDI1'] = pass_ISDI1
simulator_dict['pass_ISDI2'] = pass_ISDI2
simulator_dict['pass_ISDND'] = pass_ISDND
simulator_dict['pass_ISDD'] = pass_ISDD
simulator_dict['pass_tot'] = pass_tot
simulator_dict['FE_trans'] = FE_trans
simulator_dict['tot_D'] = tot_D
simulator_dict['dist_tot'] = dist_tot

subheader7 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Données & Bilan CO2e 🌍</p>
</head>
'''
st.markdown(subheader7, unsafe_allow_html=True)
E_ISDI1 = round((ISDI1 * FEterres) / 1000, 1)
E_ISDI2 = round((ISDI2 * FEgravats) / 1000, 1)
E_ISDND = round((ISDND * FEdnd) / 1000, 1)
E_ISDD = round((ISDD * FEdd) / 1000, 1)
E_trans_ISDI1 = round(
    FE_trans * dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1), 1)
E_trans_ISDI2 = round(
    FE_trans * dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2), 1)
E_trans_ISDND = round(
    FE_trans * dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND), 1)
E_trans_ISDD = round(
    FE_trans * dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD), 1)
E_trans = round(FE_trans * (
        dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
        + dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
        + dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
        + dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD)),1)
E_valo = E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD
E_tot = E_trans + E_valo
simulator_dict['E_ISDI1'] = E_ISDI1
simulator_dict['E_ISDI2'] = E_ISDI2
simulator_dict['E_ISDND'] = E_ISDND
simulator_dict['E_ISDD'] = E_ISDD
simulator_dict['E_trans_ISDI1'] = E_trans_ISDI1
simulator_dict['E_trans_ISDI2'] = E_trans_ISDI2
simulator_dict['E_trans_ISDND'] = E_trans_ISDND
simulator_dict['E_trans_ISDD'] = E_trans_ISDD
simulator_dict['E_trans'] = E_trans
simulator_dict['E_valo'] = E_valo
simulator_dict['E_tot'] = E_tot


with st.expander("Emissions de CO2e par types de déchets :"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Terres")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(round(E_ISDI1,1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(round(E_trans_ISDI1,1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(round(E_ISDI1 + E_trans_ISDI1,1))
        if ISDI1 > 0:
            st.write("kgCO2e/tonne :")
            I_ISDI1_kgCO2T=round(((E_ISDI1 + E_trans_ISDI1) / ISDI1) * 1000,1)
            st.subheader(str(I_ISDI1_kgCO2T))
            simulator_dict['I_ISDI1_kgCO2T'] = I_ISDI1_kgCO2T
        else:
            simulator_dict['I_ISDI1_kgCO2T'] = 0
    with col2:
        st.subheader("Gravats")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(round(E_ISDI2,1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(round(E_trans_ISDI2,1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(round(E_ISDI2 + E_trans_ISDI2,1))
        if ISDI2 > 0:
            st.write("kgCO2e/tonne :")
            I_ISDI2_kgCO2T = round(((E_ISDI2 + E_trans_ISDI2) / ISDI2) * 1000, 1)
            st.subheader(str(I_ISDI2_kgCO2T))
            simulator_dict['I_ISDI2_kgCO2T'] = I_ISDI2_kgCO2T
        else:
            simulator_dict['I_ISDI2_kgCO2T'] = 0
    with col3:
        st.subheader("DND")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(round(E_ISDND,1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(round(E_trans_ISDND,1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(round(E_ISDND + E_trans_ISDND,1))
        if ISDND > 0:
            st.write("kgCO2e/tonne :")
            I_ISDND_kgCO2T = round(((E_ISDND + E_trans_ISDND) / ISDND) * 1000, 1)
            st.subheader(str(I_ISDND_kgCO2T))
            simulator_dict['I_ISDND_kgCO2T'] = I_ISDND_kgCO2T
        else:
            simulator_dict['I_ISDND_kgCO2T'] = 0
    with col4:
        st.subheader("DD")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(round(E_ISDD,1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(round(E_trans_ISDD,1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(round(E_ISDD + E_trans_ISDD,1))
        if ISDD > 0:
            st.write("kgCO2e/tonne :")
            I_ISDD_kgCO2T = round(((E_ISDD + E_trans_ISDD) / ISDD) * 1000, 1)
            st.subheader(str(I_ISDD_kgCO2T))
            simulator_dict['I_ISDD_kgCO2T'] = I_ISDD_kgCO2T
        else:
            simulator_dict['I_ISDD_kgCO2T'] = 0

with st.expander("Emissions totales de CO2e (en tCO2e):"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Transport :")
        st.subheader(round(E_trans,1))
    with col2:
        st.write("Traitement :")
        st.subheader(round(E_valo,1))
    with col3:
        st.write("Total des émissions :")
        st.subheader(round(E_tot,1))
    with col4:
        if tot_D > 0:
            st.write("kgCO2e/tonne :")
            I_tot_kgCO2T = round(((E_trans + E_valo) / tot_D) * 1000, 1)
            st.subheader(str(I_tot_kgCO2T))
            simulator_dict['I_tot_kgCO2T'] = I_tot_kgCO2T
        else:
            simulator_dict['I_tot_kgCO2T'] = 0

with st.expander("Distance à parcourir :"):
    st.subheader(str(dist_tot) + " km")

with st.expander("Passages :"):
    st.write("Total passages :")
    st.subheader(pass_tot)
    st.write("Total jours évacuation :")
    if pass_jour>0:
        jours_evacuation = round((pass_tot / pass_jour),1)
        simulator_dict['jours_evacuation'] = jours_evacuation
    else:
        jours_evacuation = 0
        simulator_dict['jours_evacuation'] = jours_evacuation
    st.subheader(jours_evacuation)
    st.write("Nombre de passages pour l'évacuation des terres :")
    st.subheader(pass_ISDI1)
    simulator_dict['pass_ISDI1'] = pass_ISDI1
    st.write("Nombre de passages pour l'évacuation des gravats :")
    st.subheader(pass_ISDI2)
    simulator_dict['pass_ISDI2'] = pass_ISDI2
    st.write("Nombre de passages pour l'évacuation des déchets non-dangereux :")
    st.subheader(pass_ISDND)
    simulator_dict['pass_ISDND'] = pass_ISDND
    st.write("Nombre de passages pour l'évacuation des déchets dangereux :")
    st.subheader(pass_ISDD)
    simulator_dict['pass_ISDD'] = pass_ISDD

subheader8 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Actions de réduction et gains 📉</p>
</head>
'''
st.markdown(subheader8, unsafe_allow_html=True)
#st.subheader("Actions de réduction et gains 📉")

# Réutiliser 10% des terres sur site
action1 = st.checkbox('Augmenter de 10% la réutilisation des terres sur site')
new_valo_terres = valo_terres - 10
new_ISDI1 = ISDI1brut * (new_valo_terres / 100)
new_E_ISDI1 = (new_ISDI1 * FEterres) / 1000
new_pass_ISDI1 = round((new_ISDI1 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100))),1)
new_E_trans_ISDI1 = FE_trans * dist_exuISDI1 * (
        new_ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1 + mav4e * (cam4 / 100) * new_pass_ISDI1)
new_pass_tot = new_pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
Ea1 = E_ISDI1 + E_trans_ISDI1 - new_E_ISDI1 - new_E_trans_ISDI1
conso_tot_Ea1 = conso_moy * pass_tot * dist_exuISDI1
new_conso_tot_Ea1 = conso_moy * new_pass_tot * dist_exuISDI1
eco_c_Ea1 = (conso_tot_Ea1 - new_conso_tot_Ea1) * prix_c
eco_ISDI = (pass_ISDI1 - new_pass_ISDI1) * prix_ISDI1

simulator_dict['Ea1'] = Ea1
simulator_dict['eco_c_Ea1'] = math.ceil(eco_c_Ea1)
simulator_dict['eco_ISDI'] = math.ceil(eco_ISDI)
simulator_dict['new_pass_ISDI1'] = new_pass_ISDI1
simulator_dict['new_E_trans_ISDI1'] = new_E_trans_ISDI1
simulator_dict['new_pass_tot'] = new_pass_tot


if action1:
    if valo_terres >= 10:
        v = random_CO2_equivalent(Ea1)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(str(int(Ea1)) + " tCO2e, soit " + str(
                    int((Ea1 / E_tot) * 100)) + " % des émissions totales estimées")
                st.write("soit " + v)
            else:
                st.write("Merci d'entrer au minimum une quantité de déchets")
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages (évacuation des terres) de :")
            st.subheader(str(int(pass_ISDI1 - new_pass_ISDI1)) + " passages, " + str(
                round((jours_evacuation - (new_pass_tot / pass_jour)),1)) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea1)) + " €")
            st.write("Gain € évacuation terres : ")
            st.subheader(str(math.ceil(eco_ISDI)) + " €")
    else:
        st.error("Le taux de réutilisation des terres sur site est déjà supérieur à 90%")

# Privilégier les camions 5 essieux (de 70% à 80%)
action2 = st.checkbox("Utiliser 15% de camions 5 essieux en plus")
new_cam5 = cam5 + 15
new_cam4 = 100 - new_cam5
new_FE_trans = FEmoy5e * (new_cam5 / 100) + FEmoy4e * (new_cam4 / 100)
new_E_trans_ISDI1_Ea2 = round(new_FE_trans * dist_exuISDI1 * (
        ISDI1 + mav5e * (new_cam5 / 100) * pass_ISDI1 + mav4e * (new_cam4 / 100) * pass_ISDI1), 1)
new_E_trans_ISDI2_Ea2 = round(new_FE_trans * dist_exuISDI2 * (
        ISDI2 + mav5e * (new_cam5 / 100) * pass_ISDI2 + mav4e * (new_cam4 / 100) * pass_ISDI2), 1)
new_E_trans_ISDND_Ea2 = round(new_FE_trans * dist_exuISDND * (
        ISDND + mav5e * (new_cam5 / 100) * pass_ISDND + mav4e * (new_cam4 / 100) * pass_ISDND), 1)
new_E_trans_ISDD_Ea2 = round(new_FE_trans * dist_exuISDD * (
        ISDD + mav5e * (new_cam5 / 100) * pass_ISDD + mav4e * (new_cam4 / 100) * pass_ISDD), 1)
new_pass_ISDI1_Ea2 = round((ISDI1 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDI2_Ea2 = round((ISDI2 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDND_Ea2 = round((ISDND / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDD_Ea2 = round((ISDD / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100))),1)
new_pass_tot_Ea2 = new_pass_ISDI1_Ea2 + new_pass_ISDI2_Ea2 + new_pass_ISDND_Ea2 + new_pass_ISDD_Ea2
new_E_trans_Ea2 = new_FE_trans * (dist_exuISDI1 * (
        ISDI1 + mav5e * (new_cam5 / 100) * new_pass_ISDI1_Ea2 + mav4e * (new_cam4 / 100) * new_pass_ISDI1_Ea2)
                                  + dist_exuISDI2 * (
                                          ISDI2 + mav5e * (new_cam5 / 100) * new_pass_ISDI2_Ea2 + mav4e * (
                                          new_cam4 / 100) * new_pass_ISDI2_Ea2)
                                  + dist_exuISDND * (
                                          ISDND + mav5e * (new_cam5 / 100) * new_pass_ISDND_Ea2 + mav4e * (
                                          new_cam4 / 100) * new_pass_ISDND_Ea2)
                                  + dist_exuISDD * (ISDD + mav5e * (new_cam5 / 100) * new_pass_ISDD_Ea2 + mav4e * (
                new_cam4 / 100) * new_pass_ISDD_Ea2))
Ea2 = round(E_trans - new_E_trans_Ea2, 1)
conso_tot = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (
        conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea2 = (conso_moy * new_pass_ISDI2_Ea2 * dist_exuISDI2) + (
        conso_moy * new_pass_ISDI1_Ea2 * dist_exuISDI1) + (conso_moy * new_pass_ISDND_Ea2 * dist_exuISDND) + (
                            conso_moy * new_pass_ISDD_Ea2 * dist_exuISDD)
eco_c_Ea2 = (conso_tot - new_conso_tot_Ea2) * prix_c
eco_ISDI1_Ea2 = (pass_ISDI1 - new_pass_ISDI1_Ea2) * prix_ISDI1
eco_ISDI2_Ea2 = (pass_ISDI2 - new_pass_ISDI2_Ea2) * prix_ISDI2
eco_ISDND_Ea2 = (pass_ISDND - new_pass_ISDND_Ea2) * prix_ISDND
eco_ISDD_Ea2 = (pass_ISDD - new_pass_ISDD_Ea2) * prix_ISDD
eco_D_tot_Ea2 = eco_ISDI1_Ea2 + eco_ISDI2_Ea2 + eco_ISDND_Ea2 + eco_ISDD_Ea2

simulator_dict['Ea2'] = Ea2
simulator_dict['eco_c_Ea2'] = math.ceil(eco_c_Ea2)
simulator_dict['eco_D_tot_Ea2'] = math.ceil(eco_D_tot_Ea2)
simulator_dict['new_pass_ISDI1_Ea2'] = new_pass_ISDI1_Ea2
simulator_dict['new_pass_ISDI2_Ea2'] = new_pass_ISDI2_Ea2
simulator_dict['new_pass_ISDND_Ea2'] = new_pass_ISDND_Ea2
simulator_dict['new_pass_ISDD_Ea2'] = new_pass_ISDD_Ea2
simulator_dict['new_pass_tot_Ea2'] = new_pass_tot_Ea2
simulator_dict['new_E_trans_Ea2'] = new_E_trans_Ea2

if action2:
    if cam5 <= 85:
        w = random_CO2_equivalent(Ea2)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(str(int(Ea2)) + " tCO2e, soit " + str(
                    int((Ea2 / E_tot) * 100)) + " % des émissions totales estimées")
                st.write("soit " + w)
            else:
                st.write("Merci d'entrer au minimum une quantité de déchets")
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(int(pass_tot - new_pass_tot_Ea2)) + " passages, " + str(
                round((jours_evacuation - (new_pass_tot_Ea2 / pass_jour)),1)) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea2)) + " €")
            st.write("Gain € évacuations : ")
            st.subheader(str(math.ceil(eco_D_tot_Ea2)) + " €")
    else:
        st.error("Le taux d'utilisation de 5 essieux est déjà supérieur à 85%")

# Optimiser le chargement de 2 tonnes (borner l'action)
action3 = st.checkbox('Optimiser le chargement moyen des camions de 2 tonnes')
new_load_cam5 = load_cam5 + 2
new_load_cam4 = load_cam4 + 2
new_pass_ISDI1_Ea3 = round((ISDI1 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100))),1)
new_pass_ISDI2_Ea3 = round((ISDI2 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100))),1)
new_pass_ISDND_Ea3 = round((ISDND / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100))),1)
new_pass_ISDD_Ea3 = round((ISDD / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100))),1)
new_pass_tot_Ea3 = new_pass_ISDI1_Ea3 + new_pass_ISDI2_Ea3 + new_pass_ISDND_Ea3 + new_pass_ISDD_Ea3
new_E_trans_Ea3 = FE_trans * (dist_exuISDI1 * (
        ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1_Ea3 + mav4e * (cam4 / 100) * new_pass_ISDI1_Ea3)
                              + dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * new_pass_ISDI2_Ea3 + mav4e * (
                cam4 / 100) * new_pass_ISDI2_Ea3)
                              + dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * new_pass_ISDND_Ea3 + mav4e * (
                cam4 / 100) * new_pass_ISDND_Ea3)
                              + dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * new_pass_ISDD_Ea3 + mav4e * (
                cam4 / 100) * new_pass_ISDD_Ea3))
Ea3 = E_trans - new_E_trans_Ea3
conso_tot_Ea3 = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (
        conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea3 = (conso_moy * new_pass_ISDI2_Ea3 * dist_exuISDI2) + (
        conso_moy * new_pass_ISDI1_Ea3 * dist_exuISDI1) + (conso_moy * new_pass_ISDND_Ea3 * dist_exuISDND) + (
                            conso_moy * new_pass_ISDD_Ea3 * dist_exuISDD)
eco_c_Ea3 = (conso_tot - new_conso_tot_Ea3) * prix_c
eco_ISDI1_Ea3 = (pass_ISDI1 - new_pass_ISDI1_Ea3) * prix_ISDI1
eco_ISDI2_Ea3 = (pass_ISDI2 - new_pass_ISDI2_Ea3) * prix_ISDI2
eco_ISDND_Ea3 = (pass_ISDND - new_pass_ISDND_Ea3) * prix_ISDND
eco_ISDD_Ea3 = (pass_ISDD - new_pass_ISDD_Ea3) * prix_ISDD
eco_D_tot_Ea3 = eco_ISDI1_Ea3 + eco_ISDI2_Ea3 + eco_ISDND_Ea3 + eco_ISDD_Ea3

simulator_dict['Ea3'] = Ea3
simulator_dict['eco_c_Ea3'] = math.ceil(eco_c_Ea3)
simulator_dict['eco_D_tot_Ea3'] = math.ceil(eco_D_tot_Ea3)
simulator_dict['new_pass_ISDI1_Ea3'] = new_pass_ISDI1_Ea3
simulator_dict['new_pass_ISDI2_Ea3'] = new_pass_ISDI2_Ea3
simulator_dict['new_pass_ISDND_Ea3'] = new_pass_ISDND_Ea3
simulator_dict['new_pass_ISDD_Ea3'] = new_pass_ISDD_Ea3
simulator_dict['new_pass_tot_Ea3'] = new_pass_tot_Ea3
simulator_dict['new_E_trans_Ea3'] = new_E_trans_Ea3

if action3:
    if load_cam4 <= 18 and load_cam5 <= 27:
        x = random_CO2_equivalent(Ea3)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(str(int(Ea3)) + " tCO2e, soit " + str(
                    int((Ea3 / E_tot) * 100)) + " % des émissions totales estimées")
                st.write("soit " + x)
            else:
                st.write("Merci d'entrer au minimum une quantité de déchets")
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(int(pass_tot - new_pass_tot_Ea3)) + " passages, " + str(
                round((jours_evacuation - (new_pass_tot_Ea3 / pass_jour)),1)) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea3)) + " €")
            st.write("Gain € évacuations : ")
            st.subheader(str(math.ceil(eco_D_tot_Ea3)) + " €")
    else:
        st.error("Le chargement maximal est dépassé")

# Choix d'un exutoire 10 km plus proche
action4 = st.checkbox("Choisir un exutoire 10 km plus proche")
new_dist_exuISDI1 = dist_exuISDI1 - 10
new_dist_exuISDI2 = dist_exuISDI2 - 10
new_dist_exuISDND = dist_exuISDND - 10
new_dist_exuISDD = dist_exuISDD - 10
new_E_trans_Ea4 = FE_trans * (
        new_dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
        + new_dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
        + new_dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
        + new_dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD))
Ea4 = E_trans - new_E_trans_Ea4
conso_tot_Ea4 = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (
        conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea4 = (conso_moy * pass_ISDI2 * new_dist_exuISDI2) + (conso_moy * pass_ISDI1 * new_dist_exuISDI1) + (
        conso_moy * pass_ISDND * new_dist_exuISDND) + (conso_moy * pass_ISDD * new_dist_exuISDD)
eco_c_Ea4 = (conso_tot - new_conso_tot_Ea4) * prix_c

simulator_dict['Ea4'] = Ea4
simulator_dict['eco_c_Ea4'] = math.ceil(eco_c_Ea4)

if action4:
    if dist_exuISDI1 >= 10 and dist_exuISDI2 >= 10 and dist_exuISDND >= 10 and dist_exuISDD >= 10:
        y = random_CO2_equivalent(Ea4)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(str(int(Ea4)) + " tCO2e, soit " + str(
                    int((Ea4 / E_tot) * 100)) + " % des émissions totales estimées")
                st.write("soit " + y)
            else:
                st.write("Merci d'entrer au minimum une quantité de déchets")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea4)) + " €")
    else:
        st.error("Un des exutoires se trouve déjà à moins de 10 km du chantier")

# Toutes les actions combinées
action5 = st.checkbox("Combiner toutes les actions de réduction")
new_pass_ISDI1_Ea5 = round((new_ISDI1 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDI2_Ea5 = round((ISDI2 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDND_Ea5 = round((ISDND / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100))),1)
new_pass_ISDD_Ea5 = round((ISDD / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100))),1)
new_E_trans_Ea5 = FE_trans * (new_dist_exuISDI1 * (
        ISDI1 + mav5e * (new_cam5 / 100) * new_pass_ISDI1_Ea5 + mav4e * (new_cam4 / 100) * new_pass_ISDI1_Ea5)
                              + new_dist_exuISDI2 * (
                                      ISDI2 + mav5e * (new_cam5 / 100) * new_pass_ISDI2_Ea5 + mav4e * (
                                      new_cam4 / 100) * new_pass_ISDI2_Ea5)
                              + new_dist_exuISDND * (
                                      ISDND + mav5e * (new_cam5 / 100) * new_pass_ISDND_Ea5 + mav4e * (
                                      new_cam4 / 100) * new_pass_ISDND_Ea5)
                              + new_dist_exuISDD * (ISDD + mav5e * (new_cam5 / 100) * new_pass_ISDD_Ea5 + mav4e * (
                new_cam4 / 100) * new_pass_ISDD_Ea5))
new_tot_D = new_ISDI1 + ISDI2 + ISDND + ISDD
new_pass_tot_Ea5 = new_pass_ISDI1_Ea5 + new_pass_ISDI2_Ea5 + new_pass_ISDND_Ea5 + new_pass_ISDD_Ea5
new_E_valo = round(new_E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD, 1)
new_E_tot_Ea5 = new_E_trans_Ea5 + new_E_valo
Ea5 = E_tot - new_E_tot_Ea5
new_conso_tot_Ea5 = (conso_moy * new_pass_ISDI2_Ea5 * new_dist_exuISDI2) + (
        conso_moy * new_pass_ISDI1_Ea5 * new_dist_exuISDI1) + (
                            conso_moy * new_pass_ISDND_Ea5 * new_dist_exuISDND) + (
                            conso_moy * new_pass_ISDD_Ea5 * new_dist_exuISDD)
eco_c_Ea5 = (conso_tot - new_conso_tot_Ea5) * prix_c
eco_ISDI1_Ea5 = (pass_ISDI1 - new_pass_ISDI1_Ea5) * prix_ISDI1
eco_ISDI2_Ea5 = (pass_ISDI2 - new_pass_ISDI2_Ea5) * prix_ISDI2
eco_ISDND_Ea5 = (pass_ISDND - new_pass_ISDND_Ea5) * prix_ISDND
eco_ISDD_Ea5 = (pass_ISDD - new_pass_ISDD_Ea5) * prix_ISDD
eco_D_tot_Ea5 = eco_ISDI1_Ea5 + eco_ISDI2_Ea5 + eco_ISDND_Ea5 + eco_ISDD_Ea5

simulator_dict['Ea5'] = Ea5
simulator_dict['eco_c_Ea5'] = math.ceil(eco_c_Ea5)
simulator_dict['eco_D_tot_Ea5'] = math.ceil(eco_D_tot_Ea5)
simulator_dict['new_pass_ISDI1_Ea5'] = new_pass_ISDI1_Ea5
simulator_dict['new_pass_ISDI2_Ea5'] = new_pass_ISDI2_Ea5
simulator_dict['new_pass_ISDND_Ea5'] = new_pass_ISDND_Ea5
simulator_dict['new_pass_ISDD_Ea5'] = new_pass_ISDD_Ea5
simulator_dict['new_pass_tot_Ea5'] = new_pass_tot_Ea5
simulator_dict['new_E_trans_Ea5'] = new_E_trans_Ea5

if action5:
    z = random_CO2_equivalent(Ea5)
    with st.expander("Réduction des émissions carbone"):
        if E_tot > 0:
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(
                str(int(Ea5)) + " tCO2e, soit " + str(int((Ea5 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + z)
        else:
            st.write("Merci d'entrer au minimum une quantité de déchets")
    with st.expander("Réduction du nombre de passages"):
        st.write("Cette action permet de réduire le nombre de passages de :")
        st.subheader(str(int(pass_tot - new_pass_tot_Ea5)) + " passages, " + str(
            round((jours_evacuation - (new_pass_tot_Ea5 / pass_jour)),1)) + " jours")
    with st.expander("Estimation du gain économique €"):
        st.write("Gain € carburant : ")
        st.subheader(str(math.ceil(eco_c_Ea5)) + " €")
        st.write("Gain € évacuations : ")
        st.subheader(str(math.ceil(eco_D_tot_Ea5)) + " €")
with st.expander("Hypothèses de calcul du gain €"):
    st.caption("*Le gain économique est calculé à partir des hypothèses suivantes :")
    st.caption("- Consommation moyenne des camions : 30 L/100km")
    st.caption("- Prix d'un litre de gazole routier B7 : 2 €")
    st.caption("- Coût d'évacuation d'un chargement 'terres' : 300 €")
    st.caption("- Coût d'évacuation d'un chargement 'gravats' : 300 €")
    st.caption("- Coût d'évacuation d'un chargement 'déchets non-dangereux' : 1500 €")
    st.caption("- Coût d'évacuation d'un chargement 'déchets dangereux' : 5000 €")

subheader9 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Graphiques 📊</p>
</head>
'''
st.markdown(subheader9, unsafe_allow_html=True)
#st.subheader("Graphiques 📊")
with st.expander("Déchets"):
    col1, col2 = st.columns(2)
    with col1:
        if ISDI1 > 0 or ISDI2 > 0 or ISDND > 0 or ISDD > 0:
            labels = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes = [ISDI1, ISDI2, ISDND, ISDD]
            fig1, ax1 = plt.subplots()
            ax1.set_title("Part des déchets par 'type'",color = "#f37121", fontfamily = 'sen', size = 28)
            ax1.pie(sizes, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b", "black", "#D9D9D9"])
            ax1.axis('equal')
            legend = ax1.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Déchets")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig1)
        if E_ISDI1 > 0 or E_ISDI2 > 0 or E_ISDND > 0 or E_ISDD > 0:
            labels2 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes2 = [E_ISDI1, E_ISDI2, E_ISDND, E_ISDD]
            fig2, ax2 = plt.subplots()
            ax2.set_title("Emissions de CO2 par déchet : 'traitement'",color = "#f37121", fontfamily = 'sen', size = 28)
            ax2.pie(sizes2, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b", "black", "#D9D9D9"])
            ax2.axis('equal')
            legend = ax2.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Déchets")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig2)
        if E_trans_ISDI1 > 0 or E_trans_ISDI2 > 0 or E_trans_ISDND > 0 or E_trans_ISDD > 0:
            labels3 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes3 = [E_trans_ISDI1, E_trans_ISDI2, E_trans_ISDND, E_trans_ISDD]
            fig3, ax3 = plt.subplots()
            ax3.set_title("Emissions de CO2e par déchet : 'transport'",color = "#f37121", fontfamily = 'sen', size = 28)
            ax3.pie(sizes3, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b", "black", "#D9D9D9"])
            ax3.axis('equal')
            legend = ax3.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Déchets")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig3)
    with col2:
        if E_ISDI1 + E_trans_ISDI1 > 0 or E_ISDI2 + E_trans_ISDI2 > 0 or E_ISDND + E_trans_ISDND > 0 or E_ISDD + E_trans_ISDD > 0:
            labels4 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes4 = [E_ISDI1 + E_trans_ISDI1, E_ISDI2 + E_trans_ISDI2, E_ISDND + E_trans_ISDND,
                      E_ISDD + E_trans_ISDD]
            fig4, ax4 = plt.subplots()
            ax4.set_title("Emissions CO2e globales par déchet",color = "#f37121", fontfamily = 'sen', size = 28)
            ax4.pie(sizes4, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b", "black", "#D9D9D9"])
            ax4.axis('equal')
            legend = ax4.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Déchets")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig4)
        if E_valo > 0 or E_trans > 0:
            labels5 = 'Traitement', 'Transport'
            sizes5 = [E_valo, E_trans]
            fig5, ax5 = plt.subplots()
            ax5.set_title("Part des émissions de CO2e Traitement/Transport",color = "#f37121", fontfamily = 'sen', size = 28)
            ax5.pie(sizes5, autopct='%1.1f%%', textprops=dict(color="w"), startangle=90, shadow=True, colors = ['#f37121', "#67686b"])
            ax5.axis('equal')
            legend = ax5.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), labelcolor = "#67686b", edgecolor = "#f37121")
            legend.set_title("Déchets")
            title = legend.get_title()
            title.set_color("#67686b")
            title.set_family("sen")
            title.set_size(18)
            st.pyplot(fig5)

with st.expander("Réductions"):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    actions = ["+ 10% de terres réutilisées", "+ 15% de camions 5 essieux", "+ 2t de chargement moyen",
               "- 10km distance chantier/exutoire", "Toutes les actions"]
    valeurs = [Ea1, Ea2, Ea3, Ea4, Ea5]
    ax.set_title('Diminution des émissions CO2e par action',color = "#f37121", fontfamily = 'sen', size = 28)
    ax.set_ylabel('tCO2e', color =  "#67686b", fontfamily = 'sen', size = 18)
    ax.set_xlabel('Actions de réduction', color =  "#67686b", fontfamily = 'sen', size = 18)
    plt.xticks(rotation=45)
    ax.bar(actions, valeurs, color="#f37121", edgecolor="#67686b")
    st.pyplot(fig)

header3 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Autres déchets 🗑️ & achats 🛒</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header3, unsafe_allow_html=True)
#st.header("SCOPE 3 : Autres déchets 🗑️ & achats 🛒")
st.write("Ici, vous simulez les émissions liées à l'évacuation et traitement d'autres types de déchets et à l'achat de matières premières, équipements ou services")
st.write("Cliquer sur Rafraîchir avant de démarrer 🔄")
if st.button('Rafraîchir Scope 3'):
    scope3d = "scope3d_blank.csv"
    df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S3d[df_S3d.columns]=""
    df_S3d.to_csv('scope3d_blank.csv')
    scope3a = "scope3a_blank.csv"
    df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S3a[df_S3a.columns] = ""
    df_S3a.to_csv('scope3a_blank.csv')

with st.expander("Type de déchet ♻"):
    scope3d = "scope3d_blank.csv"
    df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.')
    bdd_d = "Base_Carbone_FE_S3.csv"
    df = pd.read_csv(bdd_d, encoding="latin1", sep=";", decimal=',')
    df = df[df['Poste'] == "Poste 11"]
    choix_fe = st.selectbox("Catégorie du déchet :", df["Nom base français"].unique())
    df = df[df['Nom base français'] == choix_fe]
    choix_attribut = st.selectbox("Déchet :", df['Spécificité 1'].unique())
    df = df[df["Spécificité 1"] == choix_attribut]
    choix_specif = st.selectbox("Type de traitement :", df['Spécificité 2'].unique())
    df = df[df["Spécificité 2"] == choix_specif]
    choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
    df = df[df["Unité français"] == choix_unite]
    for u in df["Unité français"]:
        u = u[7:].lower()
    DO = float(st.number_input("Quantité estimée (en " + u + ") : ", step=1))
    for x in df["Total poste non décomposé"]:
        x = float(x)
    for i in df["Incertitude"]:
        i = float(i)
    EMISSIONS = round(x / 1000 * DO, 2)
    INCERTITUDE = round(EMISSIONS * 0.01 * i, 2)
    POSTE = str(df['Nom base français'].unique())
    TYPE = str(df['Spécificité 1'].unique())
    #TRAIT = str(df['Spécificité 2'].unique())
    st.write(" ")
    st.write(" ")
    st.text("Emissions GES de la donnée 💨 : " + str(EMISSIONS) + " tCO2e " + "(+ ou - " + str(INCERTITUDE) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕ "):
        new = ["Scope 3", POSTE, TYPE, str(DO), u, EMISSIONS]
        with open(scope3d, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()

with st.expander("Type d'achat 🛒"):
    scope3a = "scope3a_blank.csv"
    df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.')
    bdd_a = "Base_Carbone_FE_S3.csv"
    df = pd.read_csv(bdd_a, encoding="latin1", sep=";", decimal=',')
    df = df[df['Poste'] == "Poste 9"]
    choix_fe = st.selectbox("Catégorie du bien ou service :", df["Nom base français"].unique())
    df = df[df['Nom base français'] == choix_fe]
    choix_attribut = st.selectbox("Bien ou service :", df['Spécificité 1'].unique())
    df = df[df["Spécificité 1"] == choix_attribut]
    choix_specif = st.selectbox("Spécificité :", df['Spécificité 2'].unique())
    df = df[df["Spécificité 2"] == choix_specif]
    choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
    df = df[df["Unité français"] == choix_unite]
    for u in df["Unité français"]:
        u = u[7:].lower()
    DO_a = float(st.number_input("Quantité estimée (en " + u + ") :  ", step=1))
    for x in df["Total poste non décomposé"]:
        x = float(x)
    for i in df["Incertitude"]:
        i = float(i)
    EMISSIONS_a = round(x / 1000 * DO_a, 2)
    INCERTITUDE_a = round(EMISSIONS_a * 0.01 * i, 2)
    POSTE_a = str(df['Nom base français'].unique())
    TRAIT_a = str(df['Spécificité 2'].unique())
    st.write(" ")
    st.write(" ")
    st.text("Emissions GES de la donnée 🛒 🌍 : " + str(EMISSIONS_a) + " tCO2e " + "(+ ou - " + str(
        INCERTITUDE_a) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕   "):
        new = ["Scope 3", POSTE_a, TRAIT_a, str(DO_a), u, EMISSIONS_a]
        with open(scope3a, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()

with st.expander("Résultats 📊"):
    df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S3d = df_S3d.dropna()
    df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.', index_col=0)
    df_S3a = df_S3a.dropna()
    df_S3 = pd.concat([df_S3d, df_S3a])
    st.dataframe(df_S3)
    tot_S3d = round(df_S3d["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES 🗑️ 🌍 : " + str(tot_S3d) + " tCO2e")
    tot_S3a = round(df_S3a["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES 🛒 🌍 : " + str(tot_S3a) + " tCO2e")
    tot_S3 = round(df_S3["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES du scope 3 🗑️️+🛒 🌍 : " + str(tot_S3) + " tCO2e")
    st.write(" ")

    col1, col2 = st.columns(2)
    with col1:
        if tot_S3d > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_S3d["Donnee"]
            es = df_S3d["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES liées au traitement des déchets', color = "#f37121", fontfamily = 'sen', size = 28)
            ax.set_ylabel('Emissions (tCO2e)',color =  "#67686b", fontfamily = 'sen', size = 18)
            ax.set_xlabel('Déchets',color =  "#67686b", fontfamily = 'sen', size = 18)
            plt.xticks(rotation=45)
            ax.bar(poste, es, color="#f37121", edgecolor="#67686b", linewidth = 3)
            st.pyplot(fig)
    with col2:
        if tot_S3a > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_S3a["Donnee"]
            es = df_S3a["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES liées aux achats de biens ou services', color = "#f37121", fontfamily = 'sen', size = 28)
            ax.set_ylabel('Emissions (tCO2e)',color =  "#67686b", fontfamily = 'sen', size = 18)
            ax.set_xlabel('Biens ou services',color =  "#67686b", fontfamily = 'sen', size = 18)
            plt.xticks(rotation=45)
            ax.bar(poste, es, color="#f37121", edgecolor="#67686b", linewidth = 3)
            st.pyplot(fig)

simulator_dict['tot_S3d']=tot_S3d
simulator_dict['tot_S3a']=tot_S3a

header4 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Construction de l'ouvrage 🏗️</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header4, unsafe_allow_html=True)
#st.header("SCOPE 3 : Construction de l'ouvrage 🏗️")
st.write("Ici, vous pouvez simuler les émissions liées à la construction d'un ouvrage en fonction du type d'ouvrage et de sa surface")
bdd = "data_FE_ouvrages.csv"
df = pd.read_csv(bdd, encoding="latin1", sep=";", decimal=',')
df["Type d'ouvrage"] = df["Type d'ouvrage"].astype(str)
df["Catégorie"] = df["Catégorie"].astype(str)
df["Sous catégorie 1"] = df["Sous catégorie 1"].astype(str)
df["Sous catégorie 2"] = df["Sous catégorie 2"].astype(str)
df["Unité"] = df["Unité"].astype(str)

with st.expander("Données 👷"):
    ouvrage = st.selectbox("Type d'ouvrage :", df["Type d'ouvrage"].unique())
    df = df[df["Type d'ouvrage"].str.contains(str(ouvrage))]
    categorie = st.selectbox('Choix catégorie :', df['Catégorie'].unique())
    df = df[df['Catégorie'].str.contains(str(categorie))]
    sous_categorie1 = st.selectbox('Choix de la sous-catégorie 1 :', df['Sous catégorie 1'].unique())
    df = df[df['Sous catégorie 1'].str.contains(str(sous_categorie1))]
    sous_categorie2 = st.selectbox('Choix de la sous-catégorie 2 :', df['Sous catégorie 2'].unique())
    df = df[df['Sous catégorie 2'].str.contains(str(sous_categorie2))]
    st.dataframe(df, 1000, 150)
    for u in df["Unité"]:
        u = u[7:].lower()
    DO_ouv = float(st.number_input("Donnée opérationnelle (en " + u + ") : ", step=1))
    for x in df["FE"]:
        x = float(x)
    for i in df["Incertitude"]:
        i = float(i)
    EMISSIONS_ouv = round(x / 1000 * DO_ouv, 2)
    INCERTITUDE_ouv = round(EMISSIONS_ouv * 0.01 * i, 2)
    st.write(" ")
with st.expander("Résultat 📊"):
    st.subheader("Emissions GES de l'ouvrage 🌍 : " + str(int(EMISSIONS_ouv)) + " tCO2e ")
    st.write("(+ ou - " + str(int(INCERTITUDE_ouv)) + " tCO2e)")

simulator_dict['ouvrage'] = ouvrage
simulator_dict['categorie_ouvrage'] = categorie
simulator_dict['sous_categorie_ouvrage1'] = sous_categorie1
simulator_dict['sous_categorie_ouvrage2'] = sous_categorie2
simulator_dict['EMISSIONS_ouv'] = EMISSIONS_ouv
simulator_dict['INCERTITUDE_ouv'] = INCERTITUDE_ouv
simulator_dict['DO_ouv'] = DO_ouv

header5 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Bilan CO2 simulé 🌍</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header5, unsafe_allow_html=True)
st.write("Ici, vous retrouvez une synthèse macroscopique de votre simulation d'émissions")
with st.expander("Résultats 📊"):
    E_S123 = EMISSIONS_ouv + E_tot + tot_S3 + tot_S1 + tot_S2
    E_S3 = EMISSIONS_ouv + E_tot + tot_S3
    st.write("Emissions GES, Scope 1 ⚡ : " + str(round(tot_S1, 1)) + " tCO2e ")
    st.write("Emissions GES, Scope 2 🛢️ : " + str(round(tot_S2, 1)) + " tCO2e ")
    st.write("Emissions GES, Scope 3 🗑️+🛒+🏗️ : " + str(round(E_S3, 1)) + " tCO2e ")
    st.write("Emissions GES totales 🌍 : " + str(round(E_S123, 1)) + " tCO2e ")
    if E_S123 > 0:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        poste = ["1", "2", "3"]
        es = [tot_S1, tot_S2, E_S3]
        ax.set_title('Emissions GES par scope', color="#f37121", fontfamily='sen', size=28)
        ax.set_ylabel('Emissions (tCO2e)', color="#67686b", fontfamily='sen', size=18)
        ax.set_xlabel('Scopes', color="#67686b", fontfamily='sen', size=18)
        plt.xticks(rotation=45)
        ax.bar(poste, es, color="#f37121", edgecolor="#67686b", linewidth=3)
        st.pyplot(fig)

simulator_dict['E_S123'] = E_S123
simulator_dict['E_S3'] = E_S3

header6 = '''
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
<p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Synthèse du bilan CO2 simulé 📋</p>
</head>
'''
st.write('---------------------------------------------------')
st.markdown(header6, unsafe_allow_html=True)
#st.header("Synthèse du bilan CO2 simulé 📋")
st.write('Et hop! je télécharge un pdf de synthèse de ma simulation')

with open("ALTAROAD_Simulateur_CO2_SYNTHESE.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()


if st.checkbox("J'accepte d'être contacté par ALTAROAD dans le cadre de l'utilisation de ce simulateur et j'indique mon email. "
               "Votre email ne sera pas diffusé en dehors de nos services."):
    email_user=st.text_input('indiquez votre email valide ici', value="", max_chars=None, key=None, type="default")
    simulator_dict['email_user'] = email_user

    if email_user!='':
        if solve(email_user):
            # we create the pdf from the dict of simulation
            build_pdf_from_dict(simulator_dict)
            st.download_button(label="Télécharger",
                               data=PDFbyte,
                               file_name="ALTAROAD_Simulateur_CO2_SYNTHESE.pdf",
                               mime='application/octet-stream')
            #ici on envoie le dictionnaire sur un bucket S3 privé avec une clé de user qui a accès qu'à ce bucket
            #code à faire
            bucket_name = 'dataset-altaroad-public'
            #filename3 = 'simulatorco2/simulatorco2_records.csv'
            read_write_S3(bucket_name, simulator_dict, ACCESS_KEY, SECRET_KEY)
        else:
            st.write('{} est malheureusement une adresse email invalide'.format(email_user))

else:
    simulator_dict['email_user'] = "empty_email_user"

st.write("------------------------------------")
st.caption("Les données de facteurs d'émissions sont issues de la Base Carbone® de l'ADEME")
st.caption("Les autres données sources utilisées sont référencées et disponible sur demande à Altaroad")
st.caption("SimulateurCO2 v0.0 - Développé par Altaroad - CONFIDENTIEL 2022 - https://www.altaroad.com")