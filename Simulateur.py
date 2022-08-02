import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image
from csv import writer
from fpdf import FPDF
import math
import random
import datetime

col1, col2 = st.columns([1, 1])
image = Image.open("logo.png")
now = datetime.datetime.utcnow()
result = now + datetime.timedelta(hours=2)
date_heure = result.strftime("%d/%m/%Y %H:%M:%S")
date = result.strftime("%d/%m/%Y")
heure = result.strftime("%H:%M:%S")
st.text("Date et heure : " + date_heure)

with col1:
    st.title("Simulateur CO2")
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

st.header("SCOPE 1 & 2 - Estimation des consommations d'énergies 🔋")
with st.expander("Energies fossiles 🛢️"):
    scope1et2 = "simulation_S1et2.csv"
    df_S1 = pd.read_csv(scope1et2, encoding="latin1", sep=",", decimal='.')
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
        new = [POSTE, ATT, str(DO), u, EMISSIONS]
        with open(scope1et2, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()
    refresh = st.checkbox('Rafraîchir')
with st.expander("Electricité ⚡"):
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
    S2 = [(POSTE2, " ", DO2, u2, EMISSIONS2)]
    df_S2 = pd.DataFrame(S2,
                         columns=['Energie', 'Attribut', 'Quantité estimée', 'Unité', 'Emissions GES (en tCO2e)'])
    if st.button("Ajout du poste d'émissions ➕  "):
        st.text("")

with st.expander("Résultats 📊"):
    df_S1et2 = pd.concat([df_S1, df_S2])
    st.dataframe(df_S1et2)
    tot_S1 = round(df_S1["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES du scope 1 🛢️ 💨 : " + str(tot_S1) + " tCO2e")
    tot_S2 = round(df_S2["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES du scope 2 ⚡ 💨 : " + str(tot_S2) + " tCO2e")
    tot_S1et2 = round(df_S1et2["Emissions GES (en tCO2e)"].sum(), 1)
    st.text("Total des émissions GES des scopes 1 & 2 🛢️+⚡ 💨 : " + str(tot_S1et2) + " tCO2e")
    st.write(" ")

    col1, col2 = st.columns(2)
    with col1:
        if tot_S1 > 0 or tot_S2 > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_S1et2["Energie"]
            es = df_S1et2["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES du Scope 1 et 2')
            ax.set_ylabel('Emissions (tCO2e)')
            ax.set_xlabel('Donnée')
            plt.xticks(rotation=45)
            ax.bar(poste, es, color='grey', edgecolor='orange')
            st.pyplot(fig)
    with col2:
        if tot_S1 > 0 or tot_S2 > 0:
            labels = '1', '2'
            sizes = [tot_S1, tot_S2]
            fig1, ax1 = plt.subplots()
            ax1.set_title("Part des émissions GES par scope")
            ax1.pie(sizes, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            ax1.legend(labels, title="Scope :", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig1)

st.header('SCOPE3 - EVACUATION')
st.write('Ici, vous simulez les évacuations de matériaux, et leur valorisation')
col1, col2 = st.columns(2)
with col1:
    st.subheader("Quantité de déchets à évacuer 🚮")
    ISDI1brut = st.number_input("Terres à excaver (en tonnes)", step=1)
    ISDI2 = st.number_input("Déchets inertes : Gravats (en tonnes)", step=1)
    ISDND = st.number_input("Déchets non-dangereux en mélange (en tonnes)", step=1)
    ISDD = st.number_input("Déchets dangereux (en tonnes)", step=1)

with col2:
    st.subheader("Distance chantier-exutoire ↔")

    dist_exuISDI1 = st.number_input("Distance exutoire 1 (en km)", value=35, step=1)
    dist_exuISDI2 = st.number_input("Distance exutoire 2 (en km)", value=35, step=1)
    dist_exuISDND = st.number_input("Distance exutoire 3 (en km)", value=35, step=1)
    dist_exuISDD = st.number_input("Distance exutoire 4 (en km)", value=35, step=1)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Nombre de passages quotidiens 🔃")
    pass_jour = st.slider("Nombre de passages quotidien estimés", 10, 100, 50, step=5)

with col2:
    st.subheader("Taux de réemploi des terres ♻️")
    repl_terres = st.slider("Réemploi des terres sur site (%)", 0, 100, 0, step=5)
    valo_terres = 100 - repl_terres
    ISDI1 = math.ceil(ISDI1brut * (valo_terres / 100))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Types de camions 🚛")
    nb_cam5 = st.number_input("Nombre de camions 5 essieux articulés", value=20, step=1)
    nb_cam4 = st.number_input("Nombre de camions 4 essieux porteurs", value=10, step=1)
    cam5 = (nb_cam5 / (nb_cam5 + nb_cam4)) * 100
    cam4 = (nb_cam4 / (nb_cam5 + nb_cam4)) * 100
with col2:
    st.subheader("Chargements 🚚")
    load_cam5 = st.slider("Chargement moyen des camions articulés (tonnes)", 15, 29, 25, step=1)
    load_cam4 = st.slider("Chargement moyen des camions porteurs (tonnes)", 10, 20, 15, step=1)

pass_ISDI1 = math.ceil(ISDI1 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDI2 = math.ceil(ISDI2 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDND = math.ceil(ISDND / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_ISDD = math.ceil(ISDD / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
pass_tot = pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
FE_trans = FEmoy5e * (cam5 / 100) + FEmoy4e * (cam4 / 100)
tot_D = ISDI1 + ISDI2 + ISDND + ISDD
dist_tot = pass_ISDI1 * dist_exuISDI1 + pass_ISDI2 * dist_exuISDI2 + pass_ISDND * dist_exuISDND + pass_ISDD * dist_exuISDD

st.subheader("Données & Bilan CO2e 💨")
E_ISDI1 = round((ISDI1 * FEterres) / 1000, 1)
E_ISDI2 = round((ISDI2 * FEgravats) / 1000, 1)
E_ISDND = round((ISDND * FEdnd) / 1000, 1)
E_ISDD = round((ISDD * FEdd) / 1000, 1)
E_trans_ISDI1 = round(
    FE_trans * dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1), 0)
E_trans_ISDI2 = round(
    FE_trans * dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2), 0)
E_trans_ISDND = round(
    FE_trans * dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND), 0)
E_trans_ISDD = round(
    FE_trans * dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD), 0)
E_trans = FE_trans * (
        dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
        + dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
        + dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
        + dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD))

E_valo = E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD
E_tot = E_trans + E_valo
with st.expander("Emissions de CO2e par types de déchets :"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Terres")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(int(E_ISDI1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDI1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDI1 + E_trans_ISDI1))
        if ISDI1 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDI1 + E_trans_ISDI1) / ISDI1) * 1000))
    with col2:
        st.subheader("Gravats")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(int(E_ISDI2))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDI2))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDI2 + E_trans_ISDI2))
        if ISDI2 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDI2 + E_trans_ISDI2) / ISDI2) * 1000))
    with col3:
        st.subheader("DND")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(int(E_ISDND))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDND))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDND + E_trans_ISDND))
        if ISDND > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDND + E_trans_ISDND) / ISDND) * 1000))
    with col4:
        st.subheader("DD")
        st.write("CO2e traitement (en tCO2e):")
        st.subheader(int(E_ISDD))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDD))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDD + E_trans_ISDD))
        if ISDD > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDD + E_trans_ISDD) / ISDD) * 1000))

with st.expander("Emissions totales de CO2e (en tCO2e):"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Transport :")
        st.subheader(int(E_trans))
    with col2:
        st.write("Traitement :")
        st.subheader(int(E_valo))
    with col3:
        st.write("Total des émissions :")
        st.subheader(int(E_tot))
    with col4:
        if tot_D > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_trans + E_valo) / tot_D) * 1000))

with st.expander("Distance à parcourir :"):
    st.subheader(str(dist_tot) + " km")

with st.expander("Passages :"):
    st.write("Total passages :")
    st.subheader(pass_tot)
    st.write("Total jours évacuation :")
    jours_evacuation = math.ceil(pass_tot / pass_jour)
    st.subheader(jours_evacuation)
    st.write("Nombre de passages pour l'évacuation des terres :")
    st.subheader(pass_ISDI1)
    st.write("Nombre de passages pour l'évacuation des gravats :")
    st.subheader(pass_ISDI2)
    st.write("Nombre de passages pour l'évacuation des déchets non-dangereux :")
    st.subheader(pass_ISDND)
    st.write("Nombre de passages pour l'évacuation des déchets dangereux :")
    st.subheader(pass_ISDD)

st.subheader("Actions de réduction et gains 📉")

# Réutiliser 10% des terres sur site
action1 = st.checkbox('Augmenter de 10% la réutilisation des terres sur site')
new_valo_terres = valo_terres - 10
new_ISDI1 = ISDI1brut * (new_valo_terres / 100)
new_E_ISDI1 = (new_ISDI1 * FEterres) / 1000
new_pass_ISDI1 = math.ceil(new_ISDI1 / (load_cam5 * (cam5 / 100) + load_cam4 * (cam4 / 100)))
new_E_trans_ISDI1 = FE_trans * dist_exuISDI1 * (
        new_ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1 + mav4e * (cam4 / 100) * new_pass_ISDI1)
new_pass_tot = new_pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
Ea1 = E_ISDI1 + E_trans_ISDI1 - new_E_ISDI1 - new_E_trans_ISDI1
conso_tot_Ea1 = conso_moy * pass_tot * dist_exuISDI1
new_conso_tot_Ea1 = conso_moy * new_pass_tot * dist_exuISDI1
eco_c_Ea1 = (conso_tot_Ea1 - new_conso_tot_Ea1) * prix_c
eco_ISDI = (pass_ISDI1 - new_pass_ISDI1) * prix_ISDI1
if action1:
    if valo_terres >= 10:
        v = random.choice([str(math.ceil(Ea1 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea1 * 5181)) + " km en voiture (" + str(
                               math.ceil(Ea1 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea1)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea1 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea1 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea1 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea1 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea1)) + " tCO2e, soit " + str(
                int((Ea1 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + v)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages (évacuation des terres) de :")
            st.subheader(str(pass_ISDI1 - new_pass_ISDI1) + " passages, " + str(
                math.ceil(jours_evacuation - (new_pass_tot / pass_jour))) + " jours")
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
new_pass_ISDI1_Ea2 = math.ceil(ISDI1 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDI2_Ea2 = math.ceil(ISDI2 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDND_Ea2 = math.ceil(ISDND / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDD_Ea2 = math.ceil(ISDD / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
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
if action2:
    if cam5 <= 85:
        w = random.choice([str(math.ceil(Ea2 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea2 * 5181)) + " km en voiture (" + str(
                               math.ceil(Ea2 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea2)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea2 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea2 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea2 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea2 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea2)) + " tCO2e, soit " + str(
                int((Ea2 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + w)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(pass_tot - new_pass_tot_Ea2) + " passages, " + str(
                math.ceil(jours_evacuation - (new_pass_tot_Ea2 / pass_jour))) + " jours")
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
new_pass_ISDI1_Ea3 = math.ceil(ISDI1 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDI2_Ea3 = math.ceil(ISDI2 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDND_Ea3 = math.ceil(ISDND / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDD_Ea3 = math.ceil(ISDD / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
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
if action3:
    if load_cam4 <= 18 and load_cam5 <= 27:
        x = random.choice([str(math.ceil(Ea3 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea3 * 5181)) + " km en voiture (" + str(
                               math.ceil(Ea3 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea3)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea3 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea3 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea3 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea3 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea3)) + " tCO2e, soit " + str(
                int((Ea3 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + x)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(pass_tot - new_pass_tot_Ea3) + " passages, " + str(
                math.ceil(jours_evacuation - (new_pass_tot_Ea3 / pass_jour))) + " jours")
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
new_dist_exuISDI2 = dist_exuISDI1 - 10
new_dist_exuISDND = dist_exuISDI1 - 10
new_dist_exuISDD = dist_exuISDI1 - 10
new_E_trans_Ea4 = FE_trans * (
        new_dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
        + new_dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
        + new_dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
        + new_dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD))
Ea4 = E_trans - new_E_trans_Ea4
conso_tot__Ea4 = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (
        conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea4 = (conso_moy * pass_ISDI2 * new_dist_exuISDI2) + (conso_moy * pass_ISDI1 * new_dist_exuISDI1) + (
        conso_moy * pass_ISDND * new_dist_exuISDND) + (conso_moy * pass_ISDD * new_dist_exuISDD)
eco_c_Ea4 = (conso_tot - new_conso_tot_Ea4) * prix_c
if action4:
    if dist_exuISDI1 >= 10 and dist_exuISDI2 >= 10 and dist_exuISDND >= 10 and dist_exuISDD >= 10:
        y = random.choice([str(math.ceil(Ea4 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea4 * 5181)) + " km en voiture (" + str(
                               math.ceil(Ea4 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea4)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea4 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea4 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea4 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea4 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea4)) + " tCO2e, soit " + str(
                int((Ea4 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + y)
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea4)) + " €")
    else:
        st.error("Un des exutoires se trouve déjà à moins de 10 km du chantier")

# Toutes les actions combinées
action5 = st.checkbox("Combiner toutes les actions de réduction")
new_pass_ISDI1_Ea5 = math.ceil(new_ISDI1 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDI2_Ea5 = math.ceil(ISDI2 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDND_Ea5 = math.ceil(ISDND / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDD_Ea5 = math.ceil(ISDD / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
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
if action5:
    z = random.choice([str(math.ceil(Ea5 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea5 * 5181)) + " km en voiture (" + str(
                           math.ceil(Ea5 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea5)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea5 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea5 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea5 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea5 * 43)) + " jeans en coton 👖"])
    with st.expander("Réduction des émissions carbone"):
        st.write("Cette action permet de réduire les émissions totales de :")
        st.subheader(
            str(int(Ea5)) + " tCO2e, soit " + str(int((Ea5 / E_tot) * 100)) + " % des émissions totales estimées")
        st.write("soit " + z)
    with st.expander("Réduction du nombre de passages"):
        st.write("Cette action permet de réduire le nombre de passages de :")
        st.subheader(str(pass_tot - new_pass_tot_Ea5) + " passages, " + str(
            math.ceil(jours_evacuation - (new_pass_tot_Ea5 / pass_jour))) + " jours")
    with st.expander("Estimation du gain économique €"):
        st.write("Gain € carburant : ")
        st.subheader(str(math.ceil(eco_c_Ea5)) + " €")
        st.write("Gain € évacuations : ")
        st.subheader(str(math.ceil(eco_D_tot_Ea5)) + " €")
st.caption("*Le gain économique est calculé à partir des hypothèses suivantes :")
st.caption("- Consommation moyenne des camions : 30 L/100km")
st.caption("- Prix d'un litre de gazole routier B7 : 2 €")
st.caption("- Coût d'évacuation d'un chargement 'terres' : 300 €")
st.caption("- Coût d'évacuation d'un chargement 'gravats' : 300 €")
st.caption("- Coût d'évacuation d'un chargement 'déchets non-dangereux' : 1500 €")
st.caption("- Coût d'évacuation d'un chargement 'déchets dangereux' : 5000 €")

st.subheader("Graphiques 📊")
with st.expander("Déchets"):
    col1, col2 = st.columns(2)
    with col1:
        if ISDI1 > 0 or ISDI2 > 0 or ISDND > 0 or ISDD > 0:
            labels = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes = [ISDI1, ISDI2, ISDND, ISDD]
            fig1, ax1 = plt.subplots()
            ax1.set_title("Part des déchets par 'type'")
            ax1.pie(sizes, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            ax1.legend(labels, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig1)
        if E_ISDI1 > 0 or E_ISDI2 > 0 or E_ISDND > 0 or E_ISDD > 0:
            labels2 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes2 = [E_ISDI1, E_ISDI2, E_ISDND, E_ISDD]
            fig2, ax2 = plt.subplots()
            ax2.set_title("Emissions de CO2 par déchet : 'traitement'")
            ax2.pie(sizes2, autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            ax2.legend(labels2, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig2)
        if E_trans_ISDI1 > 0 or E_trans_ISDI2 > 0 or E_trans_ISDND > 0 or E_trans_ISDD > 0:
            labels3 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes3 = [E_trans_ISDI1, E_trans_ISDI2, E_trans_ISDND, E_trans_ISDD]
            fig3, ax3 = plt.subplots()
            ax3.set_title("Emissions de CO2e par déchet : 'transport'")
            ax3.pie(sizes3, autopct='%1.1f%%', startangle=90)
            ax3.axis('equal')
            ax3.legend(labels3, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig3)
    with col2:
        if E_ISDI1 + E_trans_ISDI1 > 0 or E_ISDI2 + E_trans_ISDI2 > 0 or E_ISDND + E_trans_ISDND > 0 or E_ISDD + E_trans_ISDD > 0:
            labels4 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
            sizes4 = [E_ISDI1 + E_trans_ISDI1, E_ISDI2 + E_trans_ISDI2, E_ISDND + E_trans_ISDND,
                      E_ISDD + E_trans_ISDD]
            fig4, ax4 = plt.subplots()
            ax4.set_title("Emissions CO2e globales par déchet")
            ax4.pie(sizes4, autopct='%1.1f%%', startangle=90)
            ax4.axis('equal')
            ax4.legend(labels4, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig4)
        if E_valo > 0 or E_trans > 0:
            labels5 = 'Traitement', 'Transport'
            sizes5 = [E_valo, E_trans]
            fig5, ax5 = plt.subplots()
            ax5.set_title("Part des émissions de CO2e Traitement/Transport")
            ax5.pie(sizes5, autopct='%1.1f%%', startangle=90)
            ax5.axis('equal')
            ax5.legend(labels5, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            st.pyplot(fig5)

with st.expander("Réductions"):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    actions = ["+ 10% de terres réutilisées", "+ 15% de camions 5 essieux", "+ 2t de chargement moyen",
               "- 10km distance chantier/exutoire", "Toutes les actions"]
    valeurs = [Ea1, Ea2, Ea3, Ea4, Ea5]
    ax.set_title('Diminution des émissions CO2e par action')
    ax.set_ylabel('tCO2e')
    ax.set_xlabel('Actions de réduction')
    plt.xticks(rotation=45)
    ax.bar(actions, valeurs, color='grey', edgecolor='orange')
    st.pyplot(fig)

st.header("SCOPE3 : Autres déchets 🗑️ & autres achats de biens et services 🛒")
with st.expander("Type de déchet ♻"):
    simul_dechets = "simulation_dechets.csv"
    df_d = pd.read_csv(simul_dechets, encoding="latin1", sep=",", decimal='.')
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
    TRAIT = str(df['Spécificité 2'].unique())
    st.write(" ")
    st.write(" ")
    st.text("Emissions GES de la donnée 💨 : " + str(EMISSIONS) + " tCO2e " + "(+ ou - " + str(INCERTITUDE) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕ "):
        new = [POSTE, TYPE, TRAIT, str(DO), u, EMISSIONS]
        with open(simul_dechets, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()

with st.expander("Type d'achat 🛒"):
    simul_achats = "simulation_achats.csv"
    df_a = pd.read_csv(simul_achats, encoding="latin1", sep=",", decimal='.')
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
    st.text("Emissions GES de la donnée 🛒 💨 : " + str(EMISSIONS_a) + " tCO2e " + "(+ ou - " + str(
        INCERTITUDE_a) + " tCO2e)")
    if st.button("Ajout du poste d'émissions ➕   "):
        new = [POSTE_a, TRAIT_a, str(DO_a), u, EMISSIONS_a]
        with open(simul_achats, 'a', newline='', encoding='latin1') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new)
            f_object.close()

with st.expander("Résultats 📊"):
    refresh2 = st.checkbox('Rafraîchir ')
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_d)
        tot_d = round(df_d["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES 🗑️ 💨 : " + str(tot_d) + " tCO2e")
        st.write(" ")
        if tot_d > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_d["Déchets"]
            es = df_d["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES liées au traitement des déchets')
            ax.set_ylabel('Emissions (tCO2e)')
            ax.set_xlabel('Déchets')
            plt.xticks(rotation=45)
            ax.bar(poste, es, color='grey', edgecolor='orange')
            st.pyplot(fig)
    with col2:
        st.dataframe(df_a)
        tot_a = round(df_a["Emissions GES (en tCO2e)"].sum(), 1)
        st.text("Total des émissions GES 🛒 💨 : " + str(tot_a) + " tCO2e")
        st.write(" ")
        if tot_a > 0:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            poste = df_a["Biens ou services"]
            es = df_a["Emissions GES (en tCO2e)"]
            ax.set_title('Emissions GES liées aux achats de biens ou services')
            ax.set_ylabel('Emissions (tCO2e)')
            ax.set_xlabel('Biens ou services')
            plt.xticks(rotation=45)
            ax.bar(poste, es, color='grey', edgecolor='orange')
            st.pyplot(fig)

st.header("SCOPE3: Estimation du bilan CO2 de la construction de l'ouvrage 🏗️")
st.caption("Données issues de la Base Carbone® de l'ADEME")
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
    st.subheader("Emissions GES de l'ouvrage 💨 : " + str(int(EMISSIONS_ouv)) + " tCO2e ")
    st.write("(+ ou - " + str(int(INCERTITUDE_ouv)) + " tCO2e)")

st.header("Synthèse du bilan CO2 simulé 📋")
st.write('un pdf à télécharger avec toute votre simulation')
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", size=26)
pdf.cell(200, 10, txt="Synthèse des résultats", ln=1, align='C')
pdf.set_font("Arial", size=8)
pdf.cell(200, 10, txt="Document ALTAROAD", ln=1, align='C')
pdf.set_font("Arial", size=8)
pdf.cell(200, 10, txt=date_heure, ln=1, align='C')
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=22)
pdf.cell(200, 10, txt="Evacuation des déchets du site", ln=1, align='C')

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Données d'entrée", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Terres : " + str(ISDI1) + " tonnes, chantier > exutoire : " + str(dist_exuISDI1) + " km",
         ln=5)
pdf.cell(200, 10, txt="Gravats : " + str(ISDI2) + " tonnes, chantier > exutoire : " + str(dist_exuISDI2) + " km",
         ln=6)
pdf.cell(200, 10, txt="Déchets non-dangereux : " + str(ISDND) + " tonnes, chantier > exutoire : " + str(
    dist_exuISDND) + " km", ln=7)
pdf.cell(200, 10,
         txt="Déchets dangereux : " + str(ISDD) + " tonnes, chantier > exutoire : " + str(dist_exuISDD) + " km",
         ln=8)
pdf.cell(200, 10, txt="Nombre de passages quotidien : " + str(pass_jour), ln=9)
pdf.cell(200, 10, txt="Taux de réemploi des terres : " + str(repl_terres) + "%", ln=10)
pdf.cell(200, 10, txt="Camions : 5 essieux articulés : " + str(nb_cam5) + " soit " + str(
    int(cam5)) + " % ,4 essieux porteurs : " + str(nb_cam4) + " soit " + str(int(cam4)) + " %", ln=11)
pdf.cell(200, 10,
         txt="Chargement moyen des 5 essieux : " + str(load_cam5) + " ,chargement moyen des 4 essieux : " + str(
             load_cam4), ln=12)
pdf.cell(200, 10, txt="", ln=2)

pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Données de sortie", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Distance totale à parcourir : " + str(int(dist_tot)) + " km", ln=3)
pdf.cell(200, 10, txt="Nombre total de passages : " + str(int(pass_tot)), ln=3)
pdf.cell(200, 10, txt="Nombre de jours d'évacuation : " + str(int(jours_evacuation)), ln=3)

pdf.add_page()
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Bilan CO2e", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Emissions CO2e totales estimées : " + str(int(E_tot)) + " tCO2e", ln=3)
if E_tot > 0:
    pdf.cell(200, 10, txt="Emissions CO2e totales 'Transport' : " + str(int(E_trans)) + " tCO2e, soit " + str(
        int((E_trans / E_tot) * 100)) + " %", ln=3)
    pdf.cell(200, 10, txt="Emissions CO2e totales 'Valorisation' : " + str(int(E_valo)) + " tCO2e, soit " + str(
        int((E_valo / E_tot) * 100)) + " %", ln=3)
pdf.cell(200, 10, txt="", ln=2)
pdf.cell(200, 10, txt="Emissions CO2e 'Terres' : "  "Transport = " + str(
    int(E_trans_ISDI1)) + " tCO2e; Valorisation = " + str(int(E_ISDI1)) + " tCO2e; Total = " + str(
    int(E_ISDI1 + E_trans_ISDI1)) + " tCO2e", ln=3)
pdf.cell(200, 10, txt="Emissions CO2e 'Gravats' : "  "Transport = " + str(
    int(E_trans_ISDI2)) + " tCO2e; Valorisation = " + str(int(E_ISDI2)) + " tCO2e; Total = " + str(
    int(E_ISDI2 + E_trans_ISDI2)) + " tCO2e", ln=3)
pdf.cell(200, 10,
         txt="Emissions CO2e 'DND' : "  "Transport = " + str(int(E_trans_ISDND)) + " tCO2e; Valorisation = " + str(
             int(E_ISDND)) + " tCO2e; Total = " + str(int(E_ISDND + E_trans_ISDND)) + " tCO2e", ln=3)
pdf.cell(200, 10,
         txt="Emissions CO2e 'DD' : "  "Transport = " + str(int(E_trans_ISDD)) + " tCO2e; Valorisation = " + str(
             int(E_ISDD)) + " tCO2e; Total = " + str(int(E_ISDD + E_trans_ISDD)) + " tCO2e", ln=3)

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Actions de réduction et gains", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="+ 10% de réutilisation des terres sur site : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea1)) + " tCO2e; Gain passages = " + str(
    int(pass_ISDI1 - new_pass_ISDI1)) + " soit " + str(
    math.ceil(jours_evacuation - (new_pass_tot / pass_jour))) + " jours; Gain économique = " + str(
    math.ceil(eco_c_Ea1 + eco_ISDI)) + " euros", ln=3)
pdf.cell(200, 10, txt="+ 15% de camions 5 essieux articulés : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea2)) + " tCO2e; Gain passages = " + str(
    int(pass_tot - new_pass_tot_Ea2)) + " soit " + str(
    math.ceil(jours_evacuation - (new_pass_tot_Ea2 / pass_jour))) + " jours; Gain économique = " + str(
    math.ceil(eco_c_Ea2 + eco_D_tot_Ea2)) + " euros", ln=3)
pdf.cell(200, 10, txt="+ 2 tonnes de chargement moyen : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea3)) + " tCO2e; Gain passages = " + str(
    int(pass_tot - new_pass_tot_Ea3)) + " soit " + str(
    math.ceil(jours_evacuation - (new_pass_tot_Ea3 / pass_jour))) + " jours; Gain économique = " + str(
    math.ceil(eco_c_Ea3 + eco_D_tot_Ea3)) + " euros", ln=3)
pdf.cell(200, 10, txt="- 10 km de distance à l'exutoire : ", ln=3)
pdf.cell(200, 10,
         txt="Gain CO2e = " + str(int(Ea4)) + " tCO2e; Gain économique = " + str(math.ceil(eco_c_Ea4)) + " euros",
         ln=3)
pdf.cell(200, 10, txt="Toutes les actions de réductions combinées : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea5)) + " tCO2e; Gain passages = " + str(
    int(pass_tot - new_pass_tot_Ea5)) + " soit " + str(
    math.ceil(jours_evacuation - (new_pass_tot_Ea5 / pass_jour))) + " jours; Gain économique = " + str(
    math.ceil(eco_c_Ea5 + eco_D_tot_Ea5)) + " euros", ln=3)

pdf.add_page()
pdf.set_font("Arial", "B", size=22)
pdf.cell(200, 10, txt="Scopes 1 & 2 et autres postes du Scope 3", ln=1, align='C')
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Estimations du bilan CO2 de la construction de l'ouvrage", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Selon les données de l'ADEME, la construction de ce type d'ouvrage d'une surface de " + str(
    int(DO_ouv)) + " m²,", ln=3)
pdf.cell(200, 10,
         txt="émetterait environ " + str(int(EMISSIONS_ouv)) + " tCO2e (+ ou - " + str(
             int(INCERTITUDE_ouv)) + " tCO2e).",
         ln=3)

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Estimations du bilan CO2 des Scopes 1 & 2", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Scope 1 : " + str(tot_S1) + " tCO2e", ln=5)
pdf.cell(200, 10, txt="Scope 2 : " + str(tot_S2) + " tCO2e", ln=5)
pdf.cell(200, 10, txt="Scopes 1 & 2 : " + str(tot_S1et2) + " tCO2e", ln=5)

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Estimations CO2 de l'évacuation et du traitement des autres déchets", ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Emissions GES : " + str(tot_d) + " tCO2e", ln=5)
pdf.cell(200, 10, txt="", ln=2)

pdf.set_font("Arial", "B", size=22)
pdf.cell(200, 10, txt="Estimation du blian CO2 total", ln=1, align='C')
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", 'B', size=14)

pdf.cell(200, 10, txt="Total des émissions GES : " + str(int(E_tot + EMISSIONS_ouv + tot_d + tot_S1et2)) + " tCO2e",
         ln=5)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Scope 1 : " + str(int(tot_S1)) + " tCO2e, soit " + str(
    (tot_S1 / (E_tot + EMISSIONS_ouv + tot_d + tot_S1et2)) * 100) + " %", ln=5)
pdf.cell(200, 10, txt="Scope 2 : " + str(int(tot_S2)) + " tCO2e, soit " + str(
    (tot_S2 / (E_tot + EMISSIONS_ouv + tot_d + tot_S1et2)) * 100) + " %", ln=5)
pdf.cell(200, 10, txt="Scope 3 : " + str(int(E_tot + EMISSIONS_ouv + tot_d)) + " tCO2e, soit " + str(
    round(((E_tot + EMISSIONS_ouv + tot_d) / (E_tot + EMISSIONS_ouv + tot_d + tot_S1et2)) * 100, 1)) + " %", ln=5)

pdf = pdf.output("SYNTHESE.pdf")
with open("SYNTHESE.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label="Télécharger",
                   data=PDFbyte,
                   file_name="SYNTHESE.pdf",
                   mime='application/octet-stream')
st.write("")
st.caption("Les données sources utilisées sont référencées et disponible sur demande à Altaroad")
st.caption("Développé par Altaroad - CONFIDENTIEL 2022 - https://www.altaroad.com")