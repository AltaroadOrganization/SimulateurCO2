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
from utils_simu import *
import warnings
import os
import base64

warnings.filterwarnings("ignore")
plt.set_loglevel('WARNING')

#get AWS access key and secret key
ACCESS_KEY = st.secrets["my_access_key"]["ACCESS_KEY"]
SECRET_KEY = st.secrets["my_access_key"]["SECRET_KEY"]

#we initiate results dict
simulator_dict = {}

#get the FE BDD
BDD_FE_S3, BDD_FE_S2, BDD_FE_OUV = get_dataBase_func()

def show_header(simulator_dict):
    #all the inputs and outputs are saved in a dict

    Image_title=Image.open("Banner_Linkedin.png")
    st.image(Image_title)

    col1, col2 = st.columns([1, 1])

    now = datetime.datetime.utcnow()
    result = now + datetime.timedelta(hours=2)
    date_heure = result.strftime("%d/%m/%Y %H:%M:%S")
    date = result.strftime("%d/%m/%Y")
    heure = result.strftime("%H:%M:%S")
    st.caption("début de session - Date et heure : {}".format(date_heure))
    #simulator_dict['date_heure']=date_heure
    st.session_state.date_heure = date_heure

    with col1:
        original_title = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#f37121; letter-spacing: -1px; line-height: 1.2; font-size: 40px;">Simulateur CO2 du chantier</p>
        </head>
        '''
        st.markdown(original_title, unsafe_allow_html=True)
    with col2:
        # insert altaroad logo
        SC_alta = 'https://www.altaroad.com/'
        # ebay banner
        gif_html = get_img_with_href('logo.png', SC_alta)
        st.markdown(gif_html, unsafe_allow_html=True)

    constant_dict={"FEterres" : 12, "FEgravats" : 12, "FEdnd" : 84, "FEdd" : 128, "FEmoy2e" : 0.16 / 1000,
                   "FEmoy5e" : 0.0711 / 1000, "FEmoy4e" : 0.105 / 1000,"mav5e" : 15, "mav4e" : 12, "mav2e" : 9,
                   "prix_c" : 2, "prix_ISDI1": 300, "prix_ISDI2" : 300, "prix_ISDND" : 1500, "prix_ISDD" : 5000,
                "conso_moy" : 30 / 100,"new_FEmoy5e" : 59.3/1000000, "new_FEmoy4e" :100/1000000, "new_FEmoy2e":140/1000000}


    st.write("")
    st.write("Cet outil permet de simuler et réaliser une première approximation des émissions carbone de votre chantier "
             "sur l'ensemble des SCOPES, et notamment le SCOPE 3.")
    st.write("Le simulateur offre la possibilité de modifier de nombreux paramètres afin d'optimiser les émissions "
             "carbone liées à l'évacuation et au traitement de vos déchets, il donne ainsi un aperçu des nombreux "
             "avantages et gains potentiels relatifs à l'utilisation de la plateforme Digitrack proposée "
             "par Altaroad (https://www.altaroad.com/digitrack/)")
    st.write("")

    col1, col2=st.columns(2)
    col1.write("Pour plus d'informations, téléchargez le Manifeste ici")
    with open('LeManifeste_SimulateurCO2_Altaroad.pdf', "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    col2.download_button(label="le Manifeste",
                       data=PDFbyte,
                       file_name="LeManifeste_SimulateurCO2_Altaroad.pdf",
                       mime='application/octet-stream')

    link = '[Une question ? Contactez-nous 📧!](https://www.altaroad.com/demander-une-demo/)'
    st.markdown(link, unsafe_allow_html=True)

    st.write('---------------------------------------------------')
    if st.button("Effacer toutes les données saisies",use_container_width=True):
        # Clear values from *all* all in-memory and on-disk data caches:
        # i.e. clear values from both square and cube
        st.cache_data.clear()

    header0 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Les infos du chantier</p>
    </head>
    '''
    st.write('---------------------------------------------------')
    st.markdown(header0, unsafe_allow_html=True)
    with st.expander('Précisez quelques informations sur le chantier que vous souhaitez simuler'):
        list_chantier=['CONSTRUCTION','DEMOLITION','TERRASSEMENT']
        type_chantier = st.selectbox("Type de chantier", list_chantier, list_chantier.index(st.session_state["type_chantier"]))
        lieu_chantier = st.text_input('Le lieu du chantier (entrer une adresse)', value=st.session_state["lieu_chantier"], max_chars=None, key=None, type="default")
        duree_semaine_chantier=st.text_input('Durée en  semaines', value=st.session_state["duree_semaine_chantier"], max_chars=None, key=None, type="default")
        #simulator_dict['type_chantier']=type_chantier
        #simulator_dict['lieu_chantier']=lieu_chantier
        #simulator_dict['taille_chantier']=taille_chantier
        #simulator_dict['duree_semaine_chantier']=duree_semaine_chantier
        st.session_state.type_chantier = type_chantier
        st.session_state.lieu_chantier = lieu_chantier
        st.session_state.duree_semaine_chantier = duree_semaine_chantier

    return simulator_dict

@st.cache_resource(experimental_allow_widgets=True,show_spinner=False)
def show_scope3_1(simulator_dict):
    constant_dict={"FEterres" : 12, "FEgravats" : 12, "FEdnd" : 84, "FEdd" : 128, "FEmoy2e" : 0.16 / 1000,
                   "FEmoy5e" : 0.0711 / 1000, "FEmoy4e" : 0.105 / 1000,"mav5e" : 15, "mav4e" : 12, "mav2e" : 9,
                   "prix_c" : 2, "prix_ISDI1": 300, "prix_ISDI2" : 300, "prix_ISDND" : 1500, "prix_ISDD" : 5000,
                "conso_moy" : 30 / 100,"new_FEmoy5e" : 59.3/1000000, "new_FEmoy4e" :100/1000000, "new_FEmoy2e":140/1000000}

    header2 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Evacuation des déchets 🚛 </p>
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
        <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Quantité de déchets à évacuer 🚛</p>
        </head>
        '''
        st.markdown(subheader1, unsafe_allow_html=True)
        #st.subheader("Quantité de déchets à évacuer 🚮")
        ISDND = st.number_input("Déchets non-dangereux (Bois, Métaux, ...) (en T)", value=int(st.session_state['ISDD']),step=1)
        ISDI1brut = st.number_input("Déchets inertes excavés (Terres) (en T)", value=int(st.session_state['ISDI1brut']), step=1)
        ISDI2brut = st.number_input("Déchets inertes excavés (Gravats) (en T)", value=int(st.session_state['ISDI2brut']), step=1)
        ISDD = st.number_input("Déchets dangereux (en T)", value=int(st.session_state['ISDD']), step=1)
        #simulator_dict['ISDI1brut'] = ISDI1brut
        #simulator_dict['ISDI2brut'] = ISDI2brut
        #simulator_dict['ISDND'] = ISDND
        #simulator_dict['ISDD'] = ISDD
        st.session_state.ISDI1brut = ISDI1brut
        st.session_state.ISDI2brut = ISDI2brut
        st.session_state.ISDND = ISDND
        st.session_state.ISDD = ISDD


    with col2:
        subheader2 = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Distance chantier-centre de collecte</p>
        </head>
        '''
        st.markdown(subheader2, unsafe_allow_html=True)
        dist_exuISDND = st.number_input("Distance centre de collecte ISDND (en km)", value=int(st.session_state['dist_exuISDND']), step=1)
        dist_exuISDI1 = st.number_input("Distance centre de collecte ISDI1 (en km)", value=int(st.session_state['dist_exuISDI1']), step=1)
        dist_exuISDI2 = st.number_input("Distance centre de collecte ISDI2 (en km)", value=int(st.session_state['dist_exuISDI2']), step=1)
        dist_exuISDD = st.number_input("Distance centre de collecte ISDD (en km)", value=int(st.session_state['dist_exuISDD']), step=1)
        #simulator_dict['dist_exuISDI1'] = dist_exuISDI1
        #simulator_dict['dist_exuISDI2'] = dist_exuISDI2
        #simulator_dict['dist_exuISDND'] = dist_exuISDND
        #simulator_dict['dist_exuISDD'] = dist_exuISDD
        st.session_state.dist_exuISDI1 = dist_exuISDI1
        st.session_state.dist_exuISDI2 = dist_exuISDI2
        st.session_state.dist_exuISDND = dist_exuISDND
        st.session_state.dist_exuISDD = dist_exuISDD

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
        pass_jour = st.slider("Nombre de passages quotidien estimés", 10, 100, value=int(st.session_state['pass_jour']), step=5)
        #simulator_dict['pass_jour'] = pass_jour
        st.session_state.pass_jour = pass_jour

    with col2:
        subheader4 = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Réemploi des terres/gravats ♻</p>
        </head>
        '''
        st.markdown(subheader4, unsafe_allow_html=True)
        #st.subheader("Taux de réemploi des terres ♻️")
        repl_terres = st.slider("Taux de réemploi moyen sur site (%)", 0, 100, value=int(st.session_state['repl_terres']), step=5)
        valo_terres = 100 - repl_terres
        ISDI1 = math.ceil(ISDI1brut * (valo_terres / 100))
        ISDI2 = math.ceil(ISDI2brut * (valo_terres / 100))
        # simulator_dict['repl_terres'] = repl_terres
        # simulator_dict['ISDI1'] = ISDI1
        # simulator_dict['ISDI2'] = ISDI2
        st.session_state.repl_terres = repl_terres
        st.session_state.ISDI1 = ISDI1
        st.session_state.ISDI2 = ISDI2

    col1, col2 = st.columns(2)
    with col1:
        subheader5 = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Véhicules d'évacuation 🚛</p>
        </head>
        '''
        st.markdown(subheader5, unsafe_allow_html=True)
        #st.subheader("Types de camions 🚛")
        nb_cam5 = st.number_input("Nombre de camions 5 essieux articulés", value=int(st.session_state['nb_cam5']), step=1, help="Important: le facteur d'émission CO2e d'un véhicule varie selon son modèle")
        nb_cam4 = st.number_input("Nombre de camions 4 essieux porteurs", value=int(st.session_state['nb_cam4']), step=1, help="Important: le facteur d'émission CO2e d'un véhicule varie selon son modèle")
        nb_cam2 = st.number_input("Nombre de camions 2 essieux porteurs", value=int(st.session_state['nb_cam2']), step=1, help="Important: le facteur d'émission CO2e d'un véhicule varie selon son modèle")
        if (nb_cam5 + nb_cam4 + nb_cam2)>0:
            cam5 = (nb_cam5 / (nb_cam5 + nb_cam4 + nb_cam2)) * 100
            cam4 = (nb_cam4 / (nb_cam5 + nb_cam4 + nb_cam2)) * 100
            cam2 = (nb_cam2 / (nb_cam5 + nb_cam4 + nb_cam2)) * 100
            # simulator_dict['nb_cam5'] = nb_cam5
            # simulator_dict['nb_cam4'] = nb_cam4
            # simulator_dict['nb_cam2'] = nb_cam2
            # simulator_dict['cam5'] = cam5
            # simulator_dict['cam4'] = cam4
            # simulator_dict['cam2'] = cam2
            st.session_state.nb_cam5 = nb_cam5
            st.session_state.nb_cam4 = nb_cam4
            st.session_state.nb_cam2 = nb_cam2
            st.session_state.cam5 = cam5
            st.session_state.cam4 = cam4
            st.session_state.cam2 = cam2
        else:
            st.write("rentrer au moins 1 camion")
            cam2=cam5=cam4=0

    with col2:
        subheader6 = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Chargements 🚚</p>
        </head>
        '''
        st.markdown(subheader6, unsafe_allow_html=True)
        load_cam5 = st.slider("Chargement moyen des camions 5 essieux (tonnes)", 15, 29, value=int(st.session_state['load_cam5']),step=1, help="Important: optimiser le chargement permet de réduire le nombre de trajets et donc le CO2")
        load_cam4 = st.slider("Chargement moyen des camions 4 essieux (tonnes)", 10, 20, value=int(st.session_state['load_cam4']), step=1, help="Important: optimiser le chargement permet de réduire le nombre de trajets et donc le CO2")
        load_cam2 = st.slider("Chargement moyen des camions 2 essieux (tonnes)", 2, 15, value=int(st.session_state['load_cam2']), step=1, help="Important: optimiser le chargement permet de réduire le nombre de trajets et donc le CO2")
        # simulator_dict['load_cam5'] = load_cam5
        # simulator_dict['load_cam4'] = load_cam4
        # simulator_dict['load_cam2'] = load_cam2
        st.session_state.load_cam5 = load_cam5
        st.session_state.load_cam4 = load_cam4
        st.session_state.load_cam2 = load_cam2

    mean_load=(load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100) + load_cam2 * (cam2 / 100))

    if mean_load >0:
        pass_ISDI1 = math.ceil(ISDI1 / mean_load)
        pass_ISDI2 = math.ceil(ISDI2 / mean_load)
        pass_ISDND = math.ceil(ISDND / mean_load)
        pass_ISDD = math.ceil(ISDD / mean_load)
        pass_tot = pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
        FE_trans = constant_dict["FEmoy5e"] * (cam5 / 100) + constant_dict["FEmoy4e"] * (cam4 / 100) + constant_dict["FEmoy2e"] * (cam2/100)
        mav_trans = constant_dict["mav5e"] * (cam5 / 100) + constant_dict["mav4e"] * (cam4 / 100) + constant_dict["mav2e"] * (cam2/100)
        tot_D = ISDI1 + ISDI2 + ISDND + ISDD
        dist_tot = pass_ISDI1 * dist_exuISDI1 + pass_ISDI2 * dist_exuISDI2 + pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD
        # simulator_dict['pass_ISDI1'] = pass_ISDI1
        # simulator_dict['pass_ISDI2'] = pass_ISDI2
        # simulator_dict['pass_ISDND'] = pass_ISDND
        # simulator_dict['pass_ISDD'] = pass_ISDD
        # simulator_dict['pass_tot'] = pass_tot
        # simulator_dict['FE_trans'] = FE_trans
        # simulator_dict['mav_trans'] = mav_trans
        # simulator_dict['tot_D'] = tot_D
        # simulator_dict['dist_tot'] = dist_tot
        st.session_state.pass_ISDI1 = pass_ISDI1
        st.session_state.pass_ISDI2 = pass_ISDI2
        st.session_state.pass_ISDND = pass_ISDND
        st.session_state.pass_ISDD = pass_ISDD
        st.session_state.pass_tot = pass_tot
        st.session_state.FE_trans = FE_trans
        st.session_state.mav_trans = mav_trans
        st.session_state.tot_D = tot_D
        st.session_state.dist_tot = dist_tot
    else:
        st.write('rentrer au moins un camion et une masse de chargement')
        pass_ISDI1 = 0
        pass_ISDI2 = 0
        pass_ISDND = 0
        pass_ISDD = 0
        pass_tot = 0
        FE_trans = 0
        mav_trans = 0
        tot_D = 0
        dist_tot = 0

    subheader7 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Données & Bilan CO2e 🌱</p>
    </head>
    '''
    st.markdown(subheader7, unsafe_allow_html=True)
    E_ISDI1 = round((ISDI1 * constant_dict["FEterres"]) / 1000, 1)
    E_ISDI2 = round((ISDI2 * constant_dict["FEgravats"]) / 1000, 1)
    E_ISDND = round((ISDND * constant_dict["FEdnd"]) / 1000, 1)
    E_ISDD = round((ISDD * constant_dict["FEdd"]) / 1000, 1)
    E_trans_ISDI1 = round(FE_trans * dist_exuISDI1 * (ISDI1 + mav_trans * pass_ISDI1), 1)
    E_trans_ISDI2 = round(FE_trans * dist_exuISDI2 * (ISDI2 + mav_trans * pass_ISDI2), 1)
    E_trans_ISDND = round(FE_trans * dist_exuISDND * (ISDND + mav_trans * pass_ISDND), 1)
    E_trans_ISDD = round(FE_trans * dist_exuISDD * (ISDD + mav_trans * pass_ISDD), 1)
    E_trans = round(E_trans_ISDI1+E_trans_ISDI2+E_trans_ISDND+E_trans_ISDD, 1)
    E_valo = E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD
    E_tot = E_trans + E_valo
    # simulator_dict['E_ISDI1'] = E_ISDI1
    # simulator_dict['E_ISDI2'] = E_ISDI2
    # simulator_dict['E_ISDND'] = E_ISDND
    # simulator_dict['E_ISDD'] = E_ISDD
    # simulator_dict['E_trans_ISDI1'] = E_trans_ISDI1
    # simulator_dict['E_trans_ISDI2'] = E_trans_ISDI2
    # simulator_dict['E_trans_ISDND'] = E_trans_ISDND
    # simulator_dict['E_trans_ISDD'] = E_trans_ISDD
    # simulator_dict['E_trans'] = E_trans
    # simulator_dict['E_valo'] = E_valo
    # simulator_dict['E_tot'] = E_tot
    st.session_state.E_ISDI1 = E_ISDI1
    st.session_state.E_ISDI2 = E_ISDI2
    st.session_state.E_ISDND = E_ISDND
    st.session_state.E_ISDD = E_ISDD
    st.session_state.E_trans_ISDI1 = E_trans_ISDI1
    st.session_state.E_trans_ISDI2 = E_trans_ISDI2
    st.session_state.E_trans_ISDND = E_trans_ISDND
    st.session_state.E_trans_ISDD = E_trans_ISDD
    st.session_state.E_trans = E_trans
    st.session_state.E_valo = E_valo
    st.session_state.E_tot = E_tot

    with st.expander("Emissions de CO2e par types de déchets"):
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
                #simulator_dict['I_ISDI1_kgCO2T'] = I_ISDI1_kgCO2T
                st.session_state.I_ISDI1_kgCO2T = I_ISDI1_kgCO2T
            else:
                #simulator_dict['I_ISDI1_kgCO2T'] = 0
                st.session_state.I_ISDI1_kgCO2T = 0
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
                #simulator_dict['I_ISDI2_kgCO2T'] = I_ISDI2_kgCO2T
                st.session_state.I_ISDI2_kgCO2T = I_ISDI2_kgCO2T
            else:
                #simulator_dict['I_ISDI2_kgCO2T'] = 0
                st.session_state.I_ISDI1_kgCO2T = 0
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
                #simulator_dict['I_ISDND_kgCO2T'] = I_ISDND_kgCO2T
                st.session_state.I_ISDND_kgCO2T = I_ISDND_kgCO2T
            else:
                #simulator_dict['I_ISDND_kgCO2T'] = 0
                st.session_state.I_ISDND_kgCO2T = 0
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
                #simulator_dict['I_ISDD_kgCO2T'] = I_ISDD_kgCO2T
                st.session_state.I_ISDD_kgCO2T = I_ISDD_kgCO2T
            else:
                #simulator_dict['I_ISDD_kgCO2T'] = 0
                st.session_state.I_ISDD_kgCO2T = 0

    with st.expander("Emissions totales de CO2e (en tCO2e)"):
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
                #simulator_dict['I_tot_kgCO2T'] = I_tot_kgCO2T
                st.session_state.I_tot_kgCO2T = I_tot_kgCO2T
            else:
                #simulator_dict['I_tot_kgCO2T'] = 0
                st.session_state.I_tot_kgCO2T = 0

    with st.expander("Distance à parcourir"):
        st.subheader(str(dist_tot) + " km")

    with st.expander("Passages"):
        st.write("Total passages :")
        st.subheader(pass_tot)
        st.write("Total jours évacuation :")
        if pass_jour>0:
            jours_evacuation = round((pass_tot / pass_jour),1)
            #simulator_dict['jours_evacuation'] = jours_evacuation
            st.session_state.jours_evacuation = jours_evacuation
        else:
            jours_evacuation = 0
            #simulator_dict['jours_evacuation'] = jours_evacuation
            st.session_state.jours_evacuation = jours_evacuation
        st.subheader(jours_evacuation)
        st.write("Nombre de passages pour l'évacuation des terres :")
        st.subheader(pass_ISDI1)
        #simulator_dict['pass_ISDI1'] = pass_ISDI1
        st.session_state.pass_ISDI1 = pass_ISDI1
        st.write("Nombre de passages pour l'évacuation des gravats :")
        st.subheader(pass_ISDI2)
        #simulator_dict['pass_ISDI2'] = pass_ISDI2
        st.session_state.pass_ISDI2 = pass_ISDI2
        st.write("Nombre de passages pour l'évacuation des déchets non-dangereux :")
        st.subheader(pass_ISDND)
        #simulator_dict['pass_ISDND'] = pass_ISDND
        st.session_state.pass_ISDND = pass_ISDND
        st.write("Nombre de passages pour l'évacuation des déchets dangereux :")
        st.subheader(pass_ISDD)
        #simulator_dict['pass_ISDD'] = pass_ISDD
        st.session_state.pass_ISDD = pass_ISDD

    subheader8 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#f37121; font-weight: bold; letter-spacing: 0px; line-height: 1.2; font-size: 20px;">Actions de réduction et gains 📉</p>
    </head>
    '''
    st.markdown(subheader8, unsafe_allow_html=True)

    st.write("Sont ici proposées certaines des actions possibles pour la réduction du bilan CO2 SCOPE3. D'autres actions "
             "sont possibles, comme le choix du carburant. Avec ses produits, Altaroad vous aide à les mettre en place.")


    action1 = st.checkbox("ACTION 1 - Choisir une flotte de véhicules plus économes")

    new_FE_trans = constant_dict["new_FEmoy5e"] * (cam5 / 100) + constant_dict["new_FEmoy4e"] * (cam4 / 100) \
                   + constant_dict["new_FEmoy2e"] * (cam2 / 100)
    new_mav = constant_dict["mav5e"] * (cam5 / 100) + constant_dict["mav4e"] * (cam4 / 100) + constant_dict["mav2e"] * (cam2 / 100)
    new_E_trans_ISDI1_Ea2 = round(new_FE_trans * dist_exuISDI1 * (ISDI1 + new_mav * pass_ISDI1), 1)
    new_E_trans_ISDI2_Ea2 = round(new_FE_trans * dist_exuISDI2 * (ISDI2 + new_mav * pass_ISDI2), 1)
    new_E_trans_ISDND_Ea2 = round(new_FE_trans * dist_exuISDND * (ISDND + new_mav * pass_ISDND), 1)
    new_E_trans_ISDD_Ea2 = round(new_FE_trans * dist_exuISDD * (ISDD + new_mav * pass_ISDD), 1)
    new_mean_load = load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100) + load_cam2 * (cam2 / 100)
    new_pass_ISDI1_Ea2 = round((ISDI1 / new_mean_load),1)
    new_pass_ISDI2_Ea2 = round((ISDI2 / new_mean_load),1)
    new_pass_ISDND_Ea2 = round((ISDND / new_mean_load),1)
    new_pass_ISDD_Ea2 = round((ISDD / new_mean_load),1)
    new_pass_tot_Ea2 = new_pass_ISDI1_Ea2 + new_pass_ISDI2_Ea2 + new_pass_ISDND_Ea2 + new_pass_ISDD_Ea2
    new_E_trans_Ea2 = new_E_trans_ISDI1_Ea2 + new_E_trans_ISDI2_Ea2 + new_E_trans_ISDND_Ea2 + new_E_trans_ISDD_Ea2
    Ea2 = round(E_trans - new_E_trans_Ea2, 1)
    conso_tot = constant_dict["conso_moy"]*(pass_ISDI2 * dist_exuISDI2 + pass_ISDI1 * dist_exuISDI1 +
                                           pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD)
    new_conso_tot_Ea2 = constant_dict["conso_moy"]*\
                        ( new_pass_ISDI2_Ea2 * dist_exuISDI2 + new_pass_ISDI1_Ea2 * dist_exuISDI1 +
                          new_pass_ISDND_Ea2 * dist_exuISDND + new_pass_ISDD_Ea2 * dist_exuISDD)
    eco_c_Ea2 = (conso_tot - new_conso_tot_Ea2) * constant_dict["prix_c"]
    eco_ISDI1_Ea2 = (pass_ISDI1 - new_pass_ISDI1_Ea2) * constant_dict["prix_ISDI1"]
    eco_ISDI2_Ea2 = (pass_ISDI2 - new_pass_ISDI2_Ea2) * constant_dict["prix_ISDI2"]
    eco_ISDND_Ea2 = (pass_ISDND - new_pass_ISDND_Ea2) * constant_dict["prix_ISDND"]
    eco_ISDD_Ea2 = (pass_ISDD - new_pass_ISDD_Ea2) * constant_dict["prix_ISDD"]
    eco_D_tot_Ea2 = eco_ISDI1_Ea2 + eco_ISDI2_Ea2 + eco_ISDND_Ea2 + eco_ISDD_Ea2
    # simulator_dict['Ea2'] = Ea2
    # simulator_dict['eco_c_Ea2'] = math.ceil(eco_c_Ea2)
    # simulator_dict['eco_D_tot_Ea2'] = math.ceil(eco_D_tot_Ea2)
    # simulator_dict['new_pass_ISDI1_Ea2'] = new_pass_ISDI1_Ea2
    # simulator_dict['new_pass_ISDI2_Ea2'] = new_pass_ISDI2_Ea2
    # simulator_dict['new_pass_ISDND_Ea2'] = new_pass_ISDND_Ea2
    # simulator_dict['new_pass_ISDD_Ea2'] = new_pass_ISDD_Ea2
    # simulator_dict['new_pass_tot_Ea2'] = new_pass_tot_Ea2
    # simulator_dict['new_E_trans_Ea2'] = new_E_trans_Ea2
    st.session_state.Ea2 = Ea2
    st.session_state.eco_c_Ea2 = eco_c_Ea2
    st.session_state.eco_D_tot_Ea2 = eco_D_tot_Ea2
    st.session_state.new_pass_ISDI1_Ea2 = new_pass_ISDI1_Ea2
    st.session_state.new_pass_ISDI2_Ea2 = new_pass_ISDI2_Ea2
    st.session_state.new_pass_ISDND_Ea2 = new_pass_ISDND_Ea2
    st.session_state.new_pass_ISDD_Ea2 = new_pass_ISDD_Ea2
    st.session_state.new_pass_tot_Ea2 = new_pass_tot_Ea2
    st.session_state.new_E_trans_Ea2 = new_E_trans_Ea2
    
    if action1:
        st.caption("Retour d'expérience: Réduction possible de -3% à -6% du CO2e SCOPE3 total")
        st.caption("Selon la marque, le modèle "
                   "et le type de chassis, le facteur d'émission CO2e d'un camion peut varier de +/-20%. Des réductions de CO2e "
                   "totales de -3 à -6% ont alors été obtenues par le choix d'une flotte de camions plus économe. Les offres de produits Altaroad (Digitrack, Camtrack et Toptrack) "
                   "permettent par la traçabilité temps réel d'identifier ces meilleures flottes.")
        st.caption("Les meilleurs camions pour chaque type de chassis sont utilisés")
        w = random_CO2_equivalent(Ea2)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(str(round(Ea2,1)) + " tCO2e, soit " + str(
                    int((Ea2 / E_tot) * 100)) + " % des émissions totales estimées")
                st.write("soit " + w)
            else:
                st.write("Merci d'entrer au minimum une quantité de déchets")

    action2 = st.checkbox("ACTION 2 - Optimiser le chargement des camions")
    new_load_cam5 = load_cam5 + 2
    new_load_cam4 = load_cam4 + 2
    new_load_cam2 = load_cam2 + 2
    new_mean_load = (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100) + new_load_cam2 * (cam2 / 100))
    new_pass_ISDI1_Ea3 = round((ISDI1 / new_mean_load), 1)
    new_pass_ISDI2_Ea3 = round((ISDI2 / new_mean_load), 1)
    new_pass_ISDND_Ea3 = round((ISDND / new_mean_load), 1)
    new_pass_ISDD_Ea3 = round((ISDD / new_mean_load), 1)
    new_pass_tot_Ea3 = new_pass_ISDI1_Ea3 + new_pass_ISDI2_Ea3 + new_pass_ISDND_Ea3 + new_pass_ISDD_Ea3
    new_E_trans_Ea3 = FE_trans * (dist_exuISDI1 * (ISDI1 + mav_trans * new_pass_ISDI1_Ea3)
                                  + dist_exuISDI2 * (ISDI2 + mav_trans * new_pass_ISDI2_Ea3)
                                  + dist_exuISDND * (ISDND + mav_trans * new_pass_ISDND_Ea3)
                                  + dist_exuISDD * (ISDD + mav_trans * new_pass_ISDD_Ea3))
    Ea3 = E_trans - new_E_trans_Ea3
    conso_tot_Ea3 = constant_dict["conso_moy"] * (pass_ISDI2 * dist_exuISDI2 + pass_ISDI1 * dist_exuISDI1 +
                                                  pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD)
    new_conso_tot_Ea3 = constant_dict["conso_moy"] * (new_pass_ISDI2_Ea3 * dist_exuISDI2 +
                                                     new_pass_ISDI1_Ea3 * dist_exuISDI1 +
                                                     new_pass_ISDND_Ea3 * dist_exuISDND +
                                                     new_pass_ISDD_Ea3 * dist_exuISDD)
    eco_c_Ea3 = (conso_tot - new_conso_tot_Ea3) * constant_dict["prix_c"]
    eco_ISDI1_Ea3 = (pass_ISDI1 - new_pass_ISDI1_Ea3) * constant_dict["prix_ISDI1"]
    eco_ISDI2_Ea3 = (pass_ISDI2 - new_pass_ISDI2_Ea3) * constant_dict["prix_ISDI2"]
    eco_ISDND_Ea3 = (pass_ISDND - new_pass_ISDND_Ea3) * constant_dict["prix_ISDND"]
    eco_ISDD_Ea3 = (pass_ISDD - new_pass_ISDD_Ea3) * constant_dict["prix_ISDD"]
    eco_D_tot_Ea3 = eco_ISDI1_Ea3 + eco_ISDI2_Ea3 + eco_ISDND_Ea3 + eco_ISDD_Ea3

    # simulator_dict['Ea3'] = Ea3
    # simulator_dict['eco_c_Ea3'] = math.ceil(eco_c_Ea3)
    # simulator_dict['eco_D_tot_Ea3'] = math.ceil(eco_D_tot_Ea3)
    # simulator_dict['new_pass_ISDI1_Ea3'] = new_pass_ISDI1_Ea3
    # simulator_dict['new_pass_ISDI2_Ea3'] = new_pass_ISDI2_Ea3
    # simulator_dict['new_pass_ISDND_Ea3'] = new_pass_ISDND_Ea3
    # simulator_dict['new_pass_ISDD_Ea3'] = new_pass_ISDD_Ea3
    # simulator_dict['new_pass_tot_Ea3'] = new_pass_tot_Ea3
    # simulator_dict['new_E_trans_Ea3'] = new_E_trans_Ea3
    st.session_state.Ea3 = Ea3
    st.session_state.eco_c_Ea3 = eco_c_Ea3
    st.session_state.eco_D_tot_Ea3 = eco_D_tot_Ea3
    st.session_state.new_pass_ISDI1_Ea3 = new_pass_ISDI1_Ea3
    st.session_state.new_pass_ISDI2_Ea3 = new_pass_ISDI2_Ea3
    st.session_state.new_pass_ISDND_Ea3 = new_pass_ISDND_Ea3
    st.session_state.new_pass_ISDD_Ea3 = new_pass_ISDD_Ea3
    st.session_state.new_pass_tot_Ea3 = new_pass_tot_Ea3
    st.session_state.new_E_trans_Ea3 = new_E_trans_Ea3

    if action2:
        st.caption("Retour d'expérience: Réduction possible de -2% à -5% du CO2e SCOPE3 total")
        st.caption("Augmenter le chargement de la benne, "
        "permet de réduire le nombre de trajets. Cette optimisation peut se faire par une information en temps réel de la masse de chaque camion."
        " Le produit Altaroad Toptrack permet par l'information de pesée en temps réel de gagner +1 à +2T de chargement tout en évitant les surcharges.")
        st.caption("Hypothèse: +2T de chargement sur chaque chargement")
        if load_cam4 <= 18 and load_cam5 <= 27:
            x = random_CO2_equivalent(Ea3)
            with st.expander("Réduction des émissions carbone"):
                if E_tot > 0:
                    st.write("Cette action permet de réduire les émissions totales de :")
                    st.subheader(str(round(Ea3,1)) + " tCO2e, soit " + str(
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

    # Réutiliser 10% des terres sur site
    action3 = st.checkbox("ACTION 3 - Augmenter le taux de réutilisation des matériaux/déchets sur le chantier")
    new_valo_terres = valo_terres - 10
    new_ISDI1 = ISDI1brut * (new_valo_terres / 100)
    new_E_ISDI1 = (new_ISDI1 * constant_dict["FEterres"]) / 1000
    new_pass_ISDI1 = round((new_ISDI1 / mean_load),1)
    new_E_trans_ISDI1 = FE_trans * dist_exuISDI1 * (new_ISDI1 + mav_trans * new_pass_ISDI1)
    new_pass_tot = new_pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
    Ea1 = E_ISDI1 + E_trans_ISDI1 - new_E_ISDI1 - new_E_trans_ISDI1
    conso_tot_Ea1 = constant_dict["conso_moy"] * pass_tot * dist_exuISDI1
    new_conso_tot_Ea1 = constant_dict["conso_moy"] * new_pass_tot * dist_exuISDI1
    eco_c_Ea1 = (conso_tot_Ea1 - new_conso_tot_Ea1) * constant_dict["prix_c"]
    eco_ISDI = (pass_ISDI1 - new_pass_ISDI1) * constant_dict["prix_ISDI1"]

    # simulator_dict['Ea1'] = Ea1
    # simulator_dict['eco_c_Ea1'] = math.ceil(eco_c_Ea1)
    # simulator_dict['eco_ISDI'] = math.ceil(eco_ISDI)
    # simulator_dict['new_pass_ISDI1'] = new_pass_ISDI1
    # simulator_dict['new_E_trans_ISDI1'] = new_E_trans_ISDI1
    # simulator_dict['new_pass_tot'] = new_pass_tot
    st.session_state.Ea1 = Ea1
    st.session_state.eco_c_Ea1 = eco_c_Ea1
    st.session_state.eco_ISDI = eco_ISDI
    st.session_state.new_pass_ISDI1 = new_pass_ISDI1
    st.session_state.new_E_trans_ISDI1 = new_E_trans_ISDI1
    st.session_state.new_pass_tot = new_pass_tot

    if action3:
        if valo_terres >= 10:
            v = random_CO2_equivalent(Ea1)
            st.caption("Hypothèse: +10% sur le taux de valorisation choisi")
            with st.expander("Réduction des émissions carbone"):
                if E_tot > 0:
                    st.write("Cette action permet de réduire les émissions totales de :")
                    st.subheader(str(round(Ea1,1)) + " tCO2e, soit " + str(
                        int((Ea1 / E_tot) * 100)) + " % des émissions totales estimées")
                    st.write("soit " + v)
                else:
                    st.write("Merci d'entrer au minimum une quantité de déchets")
            with st.expander("Réduction du nombre de passages"):
                st.write("Cette action permet de réduire le nombre de passages d'évacuations de :")
                st.subheader(str(int(pass_ISDI1 - new_pass_ISDI1)) + " passages, " + str(
                    round((jours_evacuation - (new_pass_tot / pass_jour)),1)) + " jours")
            with st.expander("Estimation du gain économique €"):
                st.write("Gain € carburant : ")
                st.subheader(str(math.ceil(eco_c_Ea1)) + " €")
                st.write("Gain € évacuations : ")
                st.subheader(str(math.ceil(eco_ISDI)) + " €")
        else:
            st.error("Le taux de réemploi des matériaux/déchets sur site est déjà supérieur à 90%")

    # Choix d'un centre de collecte 10 km plus proche
    action4 = st.checkbox("ACTION 4 - Réduire les distances des trajets chargés")
    new_dist_exuISDI1 = dist_exuISDI1 - 10
    new_dist_exuISDI2 = dist_exuISDI2 - 10
    new_dist_exuISDND = dist_exuISDND - 10
    new_dist_exuISDD = dist_exuISDD - 10
    new_E_trans_Ea4 = FE_trans * (
            new_dist_exuISDI1 * (ISDI1 + mav_trans * pass_ISDI1)
            + new_dist_exuISDI2 * (ISDI2 + mav_trans * pass_ISDI2)
            + new_dist_exuISDND * (ISDND + mav_trans * pass_ISDND)
            + new_dist_exuISDD * (ISDD + mav_trans * pass_ISDD))
    Ea4 = E_trans - new_E_trans_Ea4
    conso_tot_Ea4 = constant_dict["conso_moy"] * (pass_ISDI2 * dist_exuISDI2 + pass_ISDI1 * dist_exuISDI1 +
                                                 pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD)
    new_conso_tot_Ea4 = constant_dict["conso_moy"] * (pass_ISDI2 * new_dist_exuISDI2 + pass_ISDI1 * new_dist_exuISDI1 +
                                                     pass_ISDND * new_dist_exuISDND + pass_ISDD * new_dist_exuISDD)
    eco_c_Ea4 = (conso_tot - new_conso_tot_Ea4) * constant_dict["prix_c"]

    # simulator_dict['Ea4'] = Ea4
    # simulator_dict['eco_c_Ea4'] = math.ceil(eco_c_Ea4)
    st.session_state.Ea4 = Ea4
    st.session_state.eco_c_Ea4 = math.ceil(eco_c_Ea4)
    

    if action4:
        st.caption("Hypothèse: choisir des centres de collecte 10 km plus proche")
        if dist_exuISDI1 >= 10 and dist_exuISDI2 >= 10 and dist_exuISDND >= 10 and dist_exuISDD >= 10:
            y = random_CO2_equivalent(Ea4)
            with st.expander("Réduction des émissions carbone"):
                if E_tot > 0:
                    st.write("Cette action permet de réduire les émissions totales de :")
                    st.subheader(str(round(Ea4,1)) + " tCO2e, soit " + str(
                        int((Ea4 / E_tot) * 100)) + " % des émissions totales estimées")
                    st.write("soit " + y)
                else:
                    st.write("Merci d'entrer au minimum une quantité de déchets")
            with st.expander("Estimation du gain économique €"):
                st.write("Gain € carburant : ")
                st.subheader(str(math.ceil(eco_c_Ea4)) + " €")
        else:
            st.error("Un des centres de collecte se trouve déjà à moins de 10 km du chantier")

    # Toutes les actions combinées
    action5 = st.checkbox("COMBINER les actions de réduction ci-dessus")
    new_mean_load_all = new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100) + new_load_cam2 * (cam2 / 100)
    new_pass_ISDI1_Ea5 = round((new_ISDI1 / new_mean_load_all),1)
    new_pass_ISDI2_Ea5 = round((ISDI2 / new_mean_load_all),1)
    new_pass_ISDND_Ea5 = round((ISDND / new_mean_load_all),1)
    new_pass_ISDD_Ea5 = round((ISDD / new_mean_load_all),1)
    new_E_trans_Ea5 = new_FE_trans * (new_dist_exuISDI1 * (ISDI1 + new_mav * new_pass_ISDI1_Ea5)
                                  + new_dist_exuISDI2 * (ISDI2 + new_mav * new_pass_ISDI2_Ea5)
                                  + new_dist_exuISDND * (ISDND + new_mav * new_pass_ISDND_Ea5)
                                  + new_dist_exuISDD * (ISDD + new_mav * new_pass_ISDD_Ea5))
    new_tot_D = new_ISDI1 + ISDI2 + ISDND + ISDD
    new_pass_tot_Ea5 = new_pass_ISDI1_Ea5 + new_pass_ISDI2_Ea5 + new_pass_ISDND_Ea5 + new_pass_ISDD_Ea5
    new_E_valo = round(new_E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD, 1)
    new_E_tot_Ea5 = new_E_trans_Ea5 + new_E_valo
    Ea5 = E_tot - new_E_tot_Ea5
    new_conso_tot_Ea5 = constant_dict["conso_moy"] * (new_pass_ISDI2_Ea5 * new_dist_exuISDI2 +
                                                     new_pass_ISDI1_Ea5 * new_dist_exuISDI1 +
                                                     new_pass_ISDND_Ea5 * new_dist_exuISDND +
                                                     new_pass_ISDD_Ea5 * new_dist_exuISDD)
    eco_c_Ea5 = (conso_tot - new_conso_tot_Ea5) * constant_dict["prix_c"]
    eco_ISDI1_Ea5 = (pass_ISDI1 - new_pass_ISDI1_Ea5) * constant_dict["prix_ISDI1"]
    eco_ISDI2_Ea5 = (pass_ISDI2 - new_pass_ISDI2_Ea5) * constant_dict["prix_ISDI2"]
    eco_ISDND_Ea5 = (pass_ISDND - new_pass_ISDND_Ea5) * constant_dict["prix_ISDND"]
    eco_ISDD_Ea5 = (pass_ISDD - new_pass_ISDD_Ea5) * constant_dict["prix_ISDD"]
    eco_D_tot_Ea5 = eco_ISDI1_Ea5 + eco_ISDI2_Ea5 + eco_ISDND_Ea5 + eco_ISDD_Ea5

    # simulator_dict['Ea5'] = Ea5
    # simulator_dict['eco_c_Ea5'] = math.ceil(eco_c_Ea5)
    # simulator_dict['eco_D_tot_Ea5'] = math.ceil(eco_D_tot_Ea5)
    # simulator_dict['new_pass_ISDI1_Ea5'] = new_pass_ISDI1_Ea5
    # simulator_dict['new_pass_ISDI2_Ea5'] = new_pass_ISDI2_Ea5
    # simulator_dict['new_pass_ISDND_Ea5'] = new_pass_ISDND_Ea5
    # simulator_dict['new_pass_ISDD_Ea5'] = new_pass_ISDD_Ea5
    # simulator_dict['new_pass_tot_Ea5'] = new_pass_tot_Ea5
    # simulator_dict['new_E_trans_Ea5'] = new_E_trans_Ea5
    st.session_state.Ea5 = Ea5
    st.session_state.eco_c_Ea5 = math.ceil(eco_c_Ea5)
    st.session_state.eco_D_tot_Ea5 = math.ceil(eco_D_tot_Ea5)
    st.session_state.new_pass_ISDI1_Ea5 = new_pass_ISDI1_Ea5
    st.session_state.new_pass_ISDI2_Ea5 = new_pass_ISDI2_Ea5
    st.session_state.new_pass_ISDND_Ea5 = new_pass_ISDND_Ea5
    st.session_state.new_pass_ISDD_Ea5 = new_pass_ISDD_Ea5
    st.session_state.new_pass_tot_Ea5 = new_pass_tot_Ea5
    st.session_state.new_E_trans_Ea5 = new_E_trans_Ea5

    if action5:
        z = random_CO2_equivalent(Ea5)
        with st.expander("Réduction des émissions carbone"):
            if E_tot > 0:
                st.write("Cette action permet de réduire les émissions totales de :")
                st.subheader(
                    str(round(Ea5,1)) + " tCO2e, soit " + str(int((Ea5 / E_tot) * 100)) + " % des émissions totales estimées")
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
        if ISDI1 > 0 or ISDI2 > 0 or ISDND > 0 or ISDD > 0:
            labels = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes = [ISDI1, ISDI2, ISDND, ISDD]
            fig1 = pie_plot(sizes, labels, "Déchets", "des masses de déchets")
            st.pyplot(fig1)
        if E_ISDI1 > 0 or E_ISDI2 > 0 or E_ISDND > 0 or E_ISDD > 0:
            labels2 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes2 = [E_ISDI1, E_ISDI2, E_ISDND, E_ISDD]
            fig2 = pie_plot(sizes2, labels2, "Déchets", "des émissions CO2e - part matière")
            st.pyplot(fig2)
        if E_trans_ISDI1 > 0 or E_trans_ISDI2 > 0 or E_trans_ISDND > 0 or E_trans_ISDD > 0:
            labels3 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes3 = [E_trans_ISDI1, E_trans_ISDI2, E_trans_ISDND, E_trans_ISDD]
            fig3 = pie_plot(sizes3, labels3, "Déchets", "des émissions CO2e - part transport")
            st.pyplot(fig3)
        if E_ISDI1 + E_trans_ISDI1 > 0 or E_ISDI2 + E_trans_ISDI2 > 0 or E_ISDND + E_trans_ISDND > 0 or E_ISDD + E_trans_ISDD > 0:
            sizes4 = [E_ISDI1 + E_trans_ISDI1, E_ISDI2 + E_trans_ISDI2, E_ISDND + E_trans_ISDND,
                      E_ISDD + E_trans_ISDD]
            labels4 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            fig4 = pie_plot(sizes4, labels4, "Déchets", "des émissions CO2e totales")
            st.pyplot(fig4)
        if E_valo > 0 or E_trans > 0:
            sizes5 = [E_valo, E_trans]
            fig5, ax5 = plt.subplots()
            labels5 = "matière", "transport"
            fig5 = pie_plot(sizes5, labels5, "part", "des émissions CO2e totales")
            st.pyplot(fig5)

    with st.expander("Réductions"):
        actions = ["Véhicules économes", "Chargement Opti.", "+ 10% taux de valo.",
                   "- 10km distance", "Toutes les actions"]
        valeurs = [Ea1, Ea2, Ea3, Ea4, Ea5]
        fig = bar_plot(valeurs, actions, 'Diminution des émissions CO2e par action', 'Actions de réduction', 'tCO2e')
        st.pyplot(fig)

    return simulator_dict

#@st.cache_resource(experimental_allow_widgets=True)
def show_scope3_2(simulator_dict):
    header3 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Autres déchets 🚛 & Livraison Matériaux 🦺</p>
    </head>
    '''
    st.write('---------------------------------------------------')
    st.markdown(header3, unsafe_allow_html=True)
    #st.header("SCOPE 3 : Autres déchets 🗑️ & achats 🛒")
    st.write("Ici, vous simulez les émissions liées à l'évacuation et traitement d'autres types de déchets et à l'achat et livraison de matières premières, équipements ou services")
    st.write("Cliquer sur Rafraîchir avant de démarrer")
    if st.button('Rafraîchir Scope 3', use_container_width=True):
        scope3d = "scope3d_blank.csv"
        df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S3d[df_S3d.columns]=""
        df_S3d.to_csv('scope3d_blank.csv')
        scope3a = "scope3a_blank.csv"
        df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S3a[df_S3a.columns] = ""
        df_S3a.to_csv('scope3a_blank.csv')

    with st.expander("Type de déchet"):
        scope3d = "scope3d_blank.csv"
        df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.')
        #bdd_d = "Base_Carbone_FE_S3.csv"
        #df = pd.read_csv(bdd_d, encoding="latin1", sep=";", decimal=',')
        df=BDD_FE_S3.copy()
        df = df[df['Poste'] == "Poste 11"]
        choix_fe = st.selectbox("Catégorie du déchet :", df["Nom base français"].unique())
        df = df[df['Nom base français'] == choix_fe]
        if df['Spécificité 1'].str.contains('/').any():
            choix_specif = st.selectbox("Type de traitement :", df['Spécificité 2'].unique())
            df = df[df["Spécificité 2"] == choix_specif]
            choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
            df = df[df["Unité français"] == choix_unite]
        else:
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
        st.text("Emissions GES de la donnée 🌱 : " + str(EMISSIONS) + " tCO2e " + "(+ ou - " + str(INCERTITUDE) + " tCO2e)")
        if st.button("Ajout du poste d'émissions ➕ "):
            new = ["Scope 3", POSTE, TYPE, str(DO), u, EMISSIONS]
            with open(scope3d, 'a', newline='', encoding='latin1') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(new)
                f_object.close()

    with st.expander("Type de Matériaux livrés 🦺"):
        scope3a = "scope3a_blank.csv"
        df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.')
        #bdd_a = "Base_Carbone_FE_S3.csv"
        #df = pd.read_csv(bdd_a, encoding="latin1", sep=";", decimal=',')
        df=BDD_FE_S3.copy()
        df = df[df['Poste'] == "Poste 9"]
        choix_fe = st.selectbox("Catégorie du bien ou service :", df["Nom base français"].unique())
        df = df[df['Nom base français'] == choix_fe]
        if df['Spécificité 1'].str.contains('/').any():
            if df['Spécificité 2'].str.contains('/').any():
                choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
                df = df[df["Unité français"] == choix_unite]
            else:
                choix_specif = st.selectbox("Spécificité :", df['Spécificité 2'].unique())
                df = df[df["Spécificité 2"] == choix_specif]
                choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
                df = df[df["Unité français"] == choix_unite]
        else:
            choix_attribut = st.selectbox("Bien ou service :", df['Spécificité 1'].unique())
            df = df[df["Spécificité 1"] == choix_attribut]
            if df['Spécificité 2'].str.contains('/').any():
                choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
                df = df[df["Unité français"] == choix_unite]
            else:
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
        st.text("Emissions GES de la donnée 🌱 : " + str(EMISSIONS_a) + " tCO2e " + "(+ ou - " + str(
            INCERTITUDE_a) + " tCO2e)")
        if st.button("Ajout du poste d'émissions ➕   "):
            new = ["Scope 3", POSTE_a, TRAIT_a, str(DO_a), u, EMISSIONS_a]
            with open(scope3a, 'a', newline='', encoding='latin1') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(new)
                f_object.close()

    with st.expander("Résultats et Graphiques 📊"):
        df_S3d = pd.read_csv(scope3d, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S3d = df_S3d.dropna()
        df_S3a = pd.read_csv(scope3a, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S3a = df_S3a.dropna()
        df_S3 = pd.concat([df_S3d, df_S3a])
        st.dataframe(df_S3)
        tot_S3d = round(df_S3d["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES autres déchets 🌱 : " + str(tot_S3d) + " tCO2e")
        tot_S3a = round(df_S3a["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES matériaux 🌱 : " + str(tot_S3a) + " tCO2e")
        tot_S3 = round(df_S3["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES du scope 3 correspondant 🌱 : " + str(tot_S3) + " tCO2e")
        st.write(" ")

        if tot_S3d > 0:
            poste = df_S3d["Donnee"]
            es = df_S3d["Emissions GES (en tCO2e)"]
            fig=bar_plot(es, poste, 'Emissions GES liées au traitement des déchets', 'Déchets', 'Emissions (tCO2e)')
            st.pyplot(fig)
        if tot_S3a > 0:
            poste = df_S3a["Donnee"]
            es = df_S3a["Emissions GES (en tCO2e)"]
            fig=bar_plot(es, poste, 'Emissions GES liées aux achats de biens ou services', 'Biens ou services', 'Emissions (tCO2e)')
            st.pyplot(fig)

    # simulator_dict['tot_S3d']=tot_S3d
    # simulator_dict['tot_S3a']=tot_S3a
    # simulator_dict['tot_S3']=tot_S3
    st.session_state.tot_S3d = tot_S3d
    st.session_state.tot_S3a = tot_S3a
    st.session_state.tot_S3 = tot_S3

    return simulator_dict

#@st.cache_resource(experimental_allow_widgets=True)
def show_scope12(simulator_dict):
    header1 = '''
        <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
        <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPES 1&2 : Consommations d'énergies ⛽</p>
        </head>
        '''
    st.write('---------------------------------------------------')
    st.markdown(header1, unsafe_allow_html=True)
    # st.header("SCOPE 1&2 : Consommations d'énergies 🔋")
    st.write(
        "Ici, vous pouvez simuler les émissions carbone directes et indirectes des Scopes 1 & 2 liées aux consommations d'énergies fossiles et d'électricité")
    st.write("Cliquer sur Rafraîchir avant de démarrer")
    if st.button('Rafraîchir Scope 1 et 2', use_container_width=True):
        scope2 = "scope2_blank.csv"
        df_S2 = pd.read_csv(scope2, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S2[df_S2.columns] = ""
        df_S2.to_csv('scope2_blank.csv')
        scope1 = "scope1_blank.csv"
        df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S1[df_S1.columns] = ""
        df_S1.to_csv('scope1_blank.csv')

    with st.expander("Scope1 - Energies fossiles ⛽"):
        scope1 = "scope1_blank.csv"
        df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S1 = df_S1.dropna()
        #bdd_s2 = "Base_Carbone_FE_S1et2.csv"
        #df = pd.read_csv(bdd_s2, encoding="latin1", sep=";", decimal=',')
        df=BDD_FE_S2.copy()
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
        if df['Nom attribut français'].str.contains('/').any():
            choix_unite = st.selectbox("Choix de l'unité :", df['Unité français'].unique())
            df = df[df["Unité français"] == choix_unite]
        else:
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
            "Emissions GES de la donnée 🌱 : " + str(EMISSIONS) + " tCO2e " + "(+ ou - " + str(INCERTITUDE) + " tCO2e)")
        if st.button("Ajout du poste d'émissions ➕"):
            new = ["Scope1", POSTE, ATT, str(DO), u, EMISSIONS]
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
        st.text("Emissions GES de la donnée 🌱 : " + str(EMISSIONS2) + " tCO2e " + "(+ ou - " + str(
            INCERTITUDE2) + " tCO2e)")
        if st.button("Ajout du poste d'émissions ➕  "):
            new2 = ["Scope2", POSTE2, "-", str(DO2), u2, EMISSIONS2]
            with open(scope2, 'a', newline='', encoding='latin1') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(new2)
                f_object.close()

    with st.expander("Résultats et Graphiques 📊"):
        df_S1 = pd.read_csv(scope1, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S1 = df_S1.dropna()
        df_S2 = pd.read_csv(scope2, encoding="latin1", sep=",", decimal='.', index_col=0)
        df_S2 = df_S2.dropna()
        df_S1et2 = pd.concat([df_S1, df_S2])
        st.dataframe(df_S1et2)
        tot_S1 = round(df_S1["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES du scope 1 ⛽ 🌱 : " + str(tot_S1) + " tCO2e")
        tot_S2 = round(df_S2["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES du scope 2 ⚡ 🌱 : " + str(tot_S2) + " tCO2e")
        tot_S1et2 = round(df_S1et2["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES des scopes 1 & 2 ⛽+⚡ 🌱 : " + str(tot_S1et2) + " tCO2e")
        st.write(" ")

        if tot_S1 > 0 or tot_S2 > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_S1et2["Donnee"]
            es = df_S1et2["Emissions GES (en tCO2e)"]
            fig = bar_plot(es, poste, 'Emissions GES des Scopes 1 et 2', 'Données', 'Emissions (tCO2e)')
            st.pyplot(fig)
        if tot_S1 > 0 or tot_S2 > 0:
            labels = '1', '2'
            sizes = [tot_S1, tot_S2]
            fig1=pie_plot(sizes, labels, "Part des émissions GES par scope", "Scope")
            st.pyplot(fig1)

    # simulator_dict['tot_S1'] = tot_S1
    # simulator_dict['tot_S2'] = tot_S2
    # simulator_dict['tot_S1et2'] = tot_S1et2
    st.session_state.tot_S1 = tot_S1
    st.session_state.tot_S2 = tot_S2
    st.session_state.tot_S1et2 = tot_S1et2

    return simulator_dict

#@st.cache_resource(experimental_allow_widgets=True)
def show_scope3_construction(simulator_dict):

    header4 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">SCOPE 3 : Construction de l'ouvrage 🏗️</p>
    </head>
    '''
    st.write('---------------------------------------------------')
    st.markdown(header4, unsafe_allow_html=True)
    st.write("Ici, vous pouvez simuler les émissions liées à la construction d'un ouvrage en fonction du type d'ouvrage et de sa surface")
    # bdd = "data_FE_ouvrages.csv"
    # df = pd.read_csv(bdd, encoding="latin1", sep=";", decimal=',')
    df=BDD_FE_OUV.copy()
    df["Type d'ouvrage"] = df["Type d'ouvrage"].astype(str)
    df["Catégorie"] = df["Catégorie"].astype(str)
    df["Sous catégorie 1"] = df["Sous catégorie 1"].astype(str)
    df["Sous catégorie 2"] = df["Sous catégorie 2"].astype(str)
    df["Unité"] = df["Unité"].astype(str)

    with st.expander("Données 👷"):
        list_ouvrage=list(df["Type d'ouvrage"].unique())
        try:
            ouvrage = st.selectbox("Type d'ouvrage :", list_ouvrage, list_ouvrage.index(st.session_state["ouvrage"]), help="Important: cette méthode d'estimation remplace l'estimation fine précédemment proposée par matériaux, déchets et énergies")
        except:
            ouvrage = st.selectbox("Type d'ouvrage :", list_ouvrage)

        df = df[df["Type d'ouvrage"].str.contains(str(ouvrage))]
        list_categorie=list(df['Catégorie'].unique())
        try:
            categorie = st.selectbox('Choix catégorie :', list_categorie, list_categorie.index(st.session_state["categorie_ouvrage"]))
        except:
            categorie = st.selectbox('Choix catégorie :', list_categorie)

        df = df[df['Catégorie'].str.contains(str(categorie))]
        list_sous_categorie1=list(df['Sous catégorie 1'].unique())
        try:
            sous_categorie1 = st.selectbox('Choix de la sous-catégorie 1 :', list_sous_categorie1, list_sous_categorie1.index(st.session_state['sous_categorie_ouvrage1']))
        except:
            sous_categorie1 = st.selectbox('Choix de la sous-catégorie 1 :', list_sous_categorie1)

        df = df[df['Sous catégorie 1'].str.contains(str(sous_categorie1))]
        if df['Sous catégorie 2'].str.contains('/').any():
            sous_categorie2 = df['Sous catégorie 2'].unique()
        else:
            list_sous_categorie2=list(df['Sous catégorie 2'].unique())
            try:
                sous_categorie2 = st.selectbox('Choix de la sous-catégorie 2 :', list_sous_categorie2, list_sous_categorie2.index(st.session_state['sous_categorie_ouvrage2']))
            except:
                sous_categorie2 = st.selectbox('Choix de la sous-catégorie 2 :', list_sous_categorie2)
            df = df[df['Sous catégorie 2'].str.contains(str(sous_categorie2))]
        #st.dataframe(df, 1000, 150)
        for u in df["Unité"]:
            u = u[7:].lower()
        DO_ouv = float(st.number_input("Donnée opérationnelle (en " + u + ") : ", value=int(st.session_state['DO_ouv']),step=1))
        for x in df["FE"]:
            x = float(x)
        for i in df["Incertitude"]:
            i = float(i)
        EMISSIONS_ouv = round(x / 1000 * DO_ouv, 2)
        INCERTITUDE_ouv = round(EMISSIONS_ouv * 0.01 * i, 2)
        st.write(" ")
    with st.expander("Résultat 📊"):
        st.subheader("Emissions GES de l'ouvrage 🌱 : " + str(int(EMISSIONS_ouv)) + " tCO2e ")
        st.write("(+ ou - " + str(int(INCERTITUDE_ouv)) + " tCO2e)")

    # simulator_dict['ouvrage'] = ouvrage
    # simulator_dict['categorie_ouvrage'] = categorie
    # simulator_dict['sous_categorie_ouvrage1'] = sous_categorie1
    # simulator_dict['sous_categorie_ouvrage2'] = sous_categorie2
    # simulator_dict['EMISSIONS_ouv'] = EMISSIONS_ouv
    # simulator_dict['INCERTITUDE_ouv'] = INCERTITUDE_ouv
    # simulator_dict['DO_ouv'] = DO_ouv
    # simulator_dict['u'] = u
    st.session_state.ouvrage = ouvrage
    st.session_state.categorie_ouvrage = categorie
    st.session_state.sous_categorie_ouvrage1 = sous_categorie1
    st.session_state.sous_categorie_ouvrage2 = sous_categorie2
    st.session_state.EMISSIONS_ouv = EMISSIONS_ouv
    st.session_state.INCERTITUDE_ouv = INCERTITUDE_ouv
    st.session_state.DO_ouv = DO_ouv
    st.session_state.u = u

    return simulator_dict

def show_co2_results(simulator_dict):
    header5 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Bilan CO2 simulé 🌱</p>
    </head>
    '''
    st.write('---------------------------------------------------')
    st.markdown(header5, unsafe_allow_html=True)
    st.write("Ici, vous retrouvez une synthèse macroscopique de votre simulation d'émissions")
    with st.expander("Résultats et Graphiques 📊"):
        # E_S123 = simulator_dict["EMISSIONS_ouv"] + simulator_dict["E_tot"] + simulator_dict["tot_S3"] + \
        #          simulator_dict["tot_S1"] + simulator_dict["tot_S2"]
        E_S123 = st.session_state["EMISSIONS_ouv"] + st.session_state["E_tot"] + st.session_state["tot_S3"] + \
                 st.session_state["tot_S1"] + st.session_state["tot_S2"]
        # E_S3 = simulator_dict["EMISSIONS_ouv"] + simulator_dict["E_tot"] + simulator_dict["tot_S3"]
        E_S3 = st.session_state["EMISSIONS_ouv"] + st.session_state["E_tot"] + st.session_state["tot_S3"]
        # simulator_dict['E_S123'] = E_S123
        # simulator_dict['E_S3'] = E_S3
        st.session_state['E_S123'] = E_S123
        st.session_state['E_S3'] = E_S3
        st.write("Emissions GES, Scope 1 ⛽ : " + str(round(st.session_state["tot_S1"], 1)) + " tCO2e ")
        st.write("Emissions GES, Scope 2 ⚡ : " + str(round(st.session_state["tot_S2"], 1)) + " tCO2e ")
        st.write("Emissions GES, Scope 3 🚛+🦺+🏗️ : " + str(round(st.session_state["E_S3"], 1)) + " tCO2e ")
        st.write("Emissions GES, Scope 3 Déchets 🚛 : " + str(round(st.session_state["E_tot"]+st.session_state["tot_S3d"], 1)) + " tCO2e ")
        st.write("Emissions GES, Scope 3 Matériaux 🦺 : " + str(round(st.session_state["tot_S3a"], 1)) + " tCO2e ")
        st.write("Emissions GES, Scope 3 Construction 🏗️ : " + str(round(st.session_state["EMISSIONS_ouv"], 1)) + " tCO2e ")

        st.write("Emissions GES totales 🌱 : " + str(round(st.session_state["E_S123"], 1)) + " tCO2e ")
        if E_S123 > 0:
            poste = ["1", "2", "3"]
            # es = [simulator_dict["tot_S1"], simulator_dict["tot_S2"], E_S3]
            es = [st.session_state["tot_S1"], st.session_state["tot_S2"], st.session_state["E_S3"]]
            fig=bar_plot(es, poste, 'Emissions GES par scope', 'Scopes', 'Emissions (tCO2e)')
            st.pyplot(fig)

    header6 = '''
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sen">
    <p style="font-family:Sen; color:#67686b; letter-spacing: -1px; line-height: 1.2; font-size: 30px;">Synthèse du bilan CO2 simulé 📋</p>
    </head>
    '''
    st.write('---------------------------------------------------')
    st.markdown(header6, unsafe_allow_html=True)
    # st.header("Synthèse du bilan CO2 simulé 📋")
    st.write('Et hop! je télécharge un pdf de synthèse de ma simulation')
    if st.checkbox(
            "J'accepte d'être contacté par ALTAROAD dans le cadre de l'utilisation de ce simulateur et j'indique mon email. "
            "Votre email ne sera pas diffusé en dehors de nos services."):
        email_user = st.text_input('indiquez votre email valide ici', value=st.session_state['email_user'], max_chars=None, key=None,
                                   type="default")
        #simulator_dict['email_user'] = email_user
        st.session_state.email_user = email_user

        if email_user != '':
            if solve(email_user):
                # we create the pdf from the dict of simulation
                st.session_state.email_user=email_user
                build_pdf_from_dict(st.session_state)
                with open("ALTAROAD_Simulateur_CO2_SYNTHESE.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(label="Télécharger",use_container_width=True,
                                   data=PDFbyte,
                                   file_name="ALTAROAD_Simulateur_CO2_SYNTHESE.pdf",
                                   mime='application/octet-stream', on_click=download_state_management(st.session_state, ACCESS_KEY, SECRET_KEY))
                # ici on envoie le dictionnaire sur un bucket S3 privé avec une clé de user qui a accès qu'à ce bucket
            else:
                st.write('{} est malheureusement une adresse email invalide'.format(email_user))

    st.write("------------------------------------")
    st.caption("Les données de facteurs d'émissions sont issues de la Base Carbone® de l'ADEME")
    st.caption("Les autres données sources utilisées sont référencées et disponible sur demande à Altaroad")
    st.caption("SimulateurCO2 v0.1 - Développé par Altaroad - CONFIDENTIEL 2023 - https://www.altaroad.com")
    return simulator_dict

if __name__ == "__main__":
    initial_dict = {
            "email_user": "",
            "nb_cam2": 4,
            "E_trans_ISDD": 0,
            "new_E_trans_Ea2": 0,
            "eco_c_Ea4": 0,
            "type_chantier": "CONSTRUCTION",
            "E_valo": 0,
            "ouvrage": " Bâtiments",
            "nb_cam5": 20,
            "tot_D": 0,
            "new_pass_ISDI2_Ea3": 0,
            "Ea3": 0,
            "ISDND": 0,
            "eco_D_tot_Ea5": 0,
            "E_tot": 0,
            "pass_jour": 50,
            "new_pass_tot_Ea2": 0,
            "repl_terres": 0,
            "cam4": 29.411764705882355,
            "Ea4": 0,
            "new_pass_ISDND_Ea2": 0,
            "new_pass_ISDD_Ea3": 0,
            "EMISSIONS_ouv": 0,
            "ISDI1": 0,
            "eco_ISDI": 0,
            "eco_c_Ea3": 0,
            "u": "m²",
            "eco_c_Ea1": 0,
            "eco_c_Ea2": 0,
            "eco_c_Ea5": 0,
            "I_ISDI1_kgCO2T": 0,
            "eco_D_tot_Ea3": 0,
            "E_trans_ISDND": 0,
            "I_ISDD_kgCO2T": 0,
            "new_pass_ISDI2_Ea2": 0,
            "E_ISDD": 0,
            "DO_ouv": 0,
            "new_E_trans_ISDI1": 0,
            "new_pass_tot_Ea3": 0,
            "jours_evacuation": 0,
            "taille_chantier": "PETIT",
            "new_pass_tot_Ea5": 0,
            "pass_ISDND": 0,
            "INCERTITUDE_ouv": 0,
            "dist_exuISDD": 35,
            "E_trans": 0,
            "load_cam5": 25,
            "tot_S2": 0,
            "ISDI1brut": 0,
            "duree_semaine_chantier": "",
            "E_trans_ISDI2": 0,
            "eco_D_tot_Ea2": 0,
            "new_pass_ISDI1_Ea3": 0,
            "download_done": False,
            "lieu_chantier": "",
            "Ea2": 0,
            "I_ISDI2_kgCO2T": 0,
            "cam2": 11.76470588235294,
            "pass_tot": 0,
            "dist_exuISDI1": 35,
            "E_ISDND": 0,
            "tot_S1et2": 0,
            "tot_S1": 0,
            "dist_tot": 0,
            "sous_categorie_ouvrage2": "array(['/'], dtype=object)",
            "cam5": 58.82352941176471,
            "new_pass_ISDD_Ea5": 0,
            "mav_trans": 13.411764705882353,
            "E_ISDI2": 0,
            "new_E_trans_Ea3": 0,
            "pass_ISDD": 0,
            "load_cam2": 8,
            "ISDD": 0,
            "pass_ISDI1": 0,
            "tot_S3a": 0,
            "new_pass_ISDI1_Ea2": 0,
            "sous_categorie_ouvrage1": "structure en béton",
            "E_S3": 0,
            "new_pass_ISDND_Ea3": 0,
            "ISDI2brut": 0,
            "E_ISDI1": 0,
            "load_cam4": 15,
            "new_pass_ISDI1_Ea5": 0,
            "new_pass_ISDD_Ea2": 0,
            "dist_exuISDI2": 35,
            "dist_exuISDND": 35,
            "E_trans_ISDI1": 0,
            "E_S123": 0,
            "I_tot_kgCO2T": 0,
            "Ea1": 0,
            "nb_cam4": 10,
            "ISDI2": 0,
            "Ea5": 0,
            "new_pass_tot": 0,
            "pass_ISDI2": 0,
            "tot_S3d": 0,
            "categorie_ouvrage": "Bâtiment agricole",
            "date_heure": "11/08/2022 16:29:18",
            "new_pass_ISDND_Ea5": 0,
            "I_ISDND_kgCO2T": 0,
            "new_E_trans_Ea5": 0,
            "new_pass_ISDI1": 0,
            "new_pass_ISDI2_Ea5": 0,
            "FE_trans": 0.00009152941176470588
        }

    #gestion de session state
    for my_key in initial_dict.keys():
        if my_key not in st.session_state:
            st.session_state[my_key] = initial_dict[my_key]

    ### the streamlit page here
    simulator_dict = show_header(simulator_dict)
    simulator_dict = show_scope3_1(simulator_dict)
    simulator_dict = show_scope3_2(simulator_dict)
    simulator_dict = show_scope12(simulator_dict)
    simulator_dict = show_scope3_construction(simulator_dict)
    simulator_dict = show_co2_results(simulator_dict)

    # #gestion de session state
    # for my_key in initial_dict.keys():
    #     if my_key not in st.session_state:
    #         st.session_state[my_key] = initial_dict[my_key]
    #     else:
    #         try:
    #             st.session_state[my_key]=simulator_dict[my_key]
    #         except:
    #             st.session_state[my_key] = initial_dict[my_key]

    if "download_done" not in st.session_state:
        st.session_state.download_done = False

