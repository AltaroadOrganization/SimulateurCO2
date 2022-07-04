import pandas as pd
import streamlit as st
import numpy as np
import dtale as dt
import matplotlib.pyplot as plt
import urllib.request
import math
from PIL import Image

urllib.request.urlretrieve("data:image/jpeg;base64,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", "alta.png")
col1, col2 = st.columns([1,1])
image = Image.open("alta.png")

with col1:
    st.title("Simulateur CO2")
    st.title("Altaroad")
with col2:
    st.image(image)

FEterres = 13
FEgravats = 26
FEdnd = 87
FEdd = 844
FEmoy5e = 0.07/1000
FEmoy4e = 0.13/1000
dist_chantier_exutoire = 45
mav5e = 14
mav4e = 13

st.header("Choix du chantier")
#Récupérer données chantier (nom, coord GPS (ou adresse))
st.header("Choix des exutoires")
#Récupérer données exutoires (nom, coord GPS (ou adresse))
#Combien d'exutoires à prendre en compte ?
#Appel openstreetmap? calul distance chantier/exutoire


st.header("Quantité de déchets à évacuer")

ISDI1 = float(st.number_input("Déchets inertes : Terres (en tonnes) : ", step=1))
ISDI2 = float(st.number_input("Déchets inertes : Gravats (en tonnes) : ", step=1))
ISDND = float(st.number_input("Déchets non-dangereux en mélange (en tonnes) :", step=1))
ISDD = float(st.number_input("Déchets dangereux (en tonnes) :", step=1))
tot_D = ISDI1+ISDI2+ISDND+ISDD

st.header("Type de camions")
cam5 = st.slider("Pourcentage de camions 5 essieux (%)",0,100,50, step=1)
cam4 = st.slider("Pourcentage de camions 4 essieux",0,100,100-cam5, step=1)

st.header("Chargement moyen")
load_cam5 = st.slider("Chargement moyen des camions 5 essieux (tonnes)",0,35,27, step=1)
load_cam4 = st.slider("Chargement moyen des camions 4 essieux (tonnes)",0,30,17, step=1)
pass_ISDI1 = math.ceil(ISDI1/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDI2 = math.ceil(ISDI2/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDND = math.ceil(ISDND/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDD = math.ceil(ISDD/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_tot = pass_ISDI1+pass_ISDI2+pass_ISDND+pass_ISDD
FE_trans = FEmoy5e*(cam5/100)+FEmoy4e*(cam4/100)

st.header("Données")

with st.expander("Distance :"):
    st.write("Nombre de km total : " + str(dist_chantier_exutoire *pass_ISDI1) + "km")

st.write("")
#pb variable pas load cam

with st.expander("Passages :"):
    st.write("Nombre de passages pour l'évacuation des terres : " + str(pass_ISDI1))
    st.write("Nombre de passages pour l'évacuation des gravats : " + str(pass_ISDI2))
    st.write("Nombre de passages pour l'évacuation des déchets non-dangereux : " + str(pass_ISDND))
    st.write("Nombre de passages pour l'évacuation des dangereux : " + str(pass_ISDD))

st.header("Bilan CO2")
E_ISDI1 = (ISDI1*FEterres)/1000
E_ISDI2 = (ISDI2*FEgravats)/1000
E_ISDND = (ISDND*FEdnd)/1000
E_ISDD = (ISDD*FEdd)/1000
E_TOT = E_ISDI1+E_ISDI2+E_ISDND+E_ISDD
E_trans_ISDI1 = FE_trans * dist_chantier_exutoire * (ISDI1 + mav5e * (cam5/100) * pass_ISDI1 + mav4e * (cam4/100) * pass_ISDI1)
E_trans_ISDI2 = FE_trans * dist_chantier_exutoire * (ISDI2 + mav5e * (cam5/100) * pass_ISDI2 + mav4e * (cam4/100) * pass_ISDI2)
E_trans_ISDND = FE_trans * dist_chantier_exutoire * (ISDND + mav5e * (cam5/100) * pass_ISDND + mav4e * (cam4/100) * pass_ISDND)
E_trans_ISDD = FE_trans * dist_chantier_exutoire * (ISDD + mav5e * (cam5/100) * pass_ISDD + mav4e * (cam4/100) * pass_ISDD)

with st.expander("Emissions de CO2e par types de déchets (en tCO2e) :"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Terres")
        st.write("CO2e valorisation :")
        st.subheader(E_ISDI1)
        st.write("CO2e transport :")
        st.subheader(E_trans_ISDI1)
        st.write("CO2e total :")
        st.subheader(E_ISDI1+E_trans_ISDI1)
        if ISDI1 > 0:
            st.write("CO2e/t :")
            st.subheader((E_ISDI1 + E_trans_ISDI1)/ISDI1)
    with col2:
        st.subheader("Gravats")
        st.write("CO2e valorisation :")
        st.subheader(E_ISDI2)
        st.write("CO2e transport :")
        st.subheader(E_trans_ISDI2)
        st.write("CO2e total :")
        st.subheader(E_ISDI2 + E_trans_ISDI2)
        if ISDI2 > 0:
            st.write("CO2e/t :")
            st.subheader((E_ISDI2 + E_trans_ISDI2) / ISDI2)
    with col3:
        st.subheader("Gravats")
        st.write("CO2e valorisation :")
        st.subheader(E_ISDND)
        st.write("CO2e transport :")
        st.subheader(E_trans_ISDND)
        st.write("CO2e total :")
        st.subheader(E_ISDND + E_trans_ISDND)
        if ISDND > 0:
            st.write("CO2e/t :")
            st.subheader((E_ISDND + E_trans_ISDND) / ISDND)
    with col4:
        st.subheader("Gravats")
        st.write("CO2e valorisation :")
        st.subheader(E_ISDD)
        st.write("CO2e transport :")
        st.subheader(E_trans_ISDD)
        st.write("CO2e total :")
        st.subheader(E_ISDD + E_trans_ISDD)
        if ISDD > 0:
            st.write("CO2e/t :")
            st.subheader((E_ISDD + E_trans_ISDD) / ISDD)


    #st.write("Emissions CO2e, valorisation des terres : " + str(E_ISDI1))
    #st.write("Emissions CO2e, valorisation des gravats : " + str(E_ISDI2))
    #st.write("Emissions CO2e, valorisation des déchets non-dangereux en mélange : " + str(E_ISDND))
    #st.write("Emissions CO2e, valorisation des déchets dangereux en mélange : " + str(E_ISDD))
    #st.write("Emissions CO2e totales liées à la valorisation des déchets : " + str(E_TOT))

with st.expander("Emissions de CO2e liées au transport des déchets (en tCO2e) :"):
    E_trans = FE_trans * dist_chantier_exutoire * (tot_D + mav5e * (cam5/100) * pass_tot + mav4e * (cam4/100) * pass_tot)
    st.write(E_trans)

with st.expander("CO2e par tonne de déchets"):
    #E_tonne =
    st.write()









st.caption("""Les données sources utilisées sont référencées et disponible sur demande à Altaroad

Développé par Altaroad - CONFIDENTIEL 2022 - https://www.altaroad.com""")