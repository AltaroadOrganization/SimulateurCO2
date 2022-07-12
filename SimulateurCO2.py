import pandas as pd
import streamlit as st
import numpy as np
import urllib.request
import math
import random
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import tempfile

urllib.request.urlretrieve("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8HDhASEBEQExASDxMRERIVGBAQEBARGBIWGBgSFRUYHSggGBolGxYWITElMS0rLi46Fx8zODMtNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAMgAyAMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABgcDBAUBAv/EADwQAAIBAgIGBgcGBgMAAAAAAAABAgMEBhEFEiExQWETIjJRcbEHUoGRocHRFCNCYnLhFjNTkqLwFUPC/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/ALxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANW70jQs195VhDxaT9wG0DVsL+lpGDnSmpx1nHNbs0R3EWMloetKiqLlKKTzckovNZgSwFX3WP7ur2I04Lwc372cm5xLfXXarz28I9XyAuOdWMN7S8WlmfZUGh7GpfV6anKUpSmt7by5+JbsY6qS7lkB9AAAAAAAAAAAAAAAAAGte3tKxjrVZxhHvbyz8O8DZPG8iDaX9IMYZxtoa3557F7I8SH6S0/daSz6SrLL1V1Y+5AXRKWqm9+zPZxIFpL0htNqjRyyeWdR7d/qok2Ea9W4sqLrRcZKOqs984rsy9qI7i3Bkrmcq1qlrSec6e7N+tH6ARa/xTe3varSin+GGUF8DkTm5vNtt97bbN2ehrqEtV0K2e7LUl5okOHcEVrmcZ3MejpJ56j7c+WS3ICU+j+1dtYQ1tjqTlUXg3kvgiDY7rKtpCtl+FRh7VHb5llaZ0lT0JbObySjHVpw9aW6MUinJyne1JSe2U5OUnzbAxQi5vJbzp2tqqO17ZeXgfdtbqgufF/LwMwEnwLadJVnUe6Ecl+p/sTg4uErT7Lawb3z679u74HaAAAAAAAAAAAAAAB43lvPmrUjRi5SaUUs23sSRWOLMXT0k3SoNxop5NrZKp+3IDvYjxxTtNanbZTqLY5vsR8O8r6/v6ukJudWcpyffw8DWPUswBO8GYQ1tWvcx2b6dJ8fzS+hmwbhDo9Wvcx62+nSf4fzS58jvYnxHT0HT4SrSXUh/6l3IDJiPT9LQVPN7ajX3dPi+b7kcbQ+PqFdJXCdKfGSTlTfu2ory/vamkKkqlWTlOW98u5LuNcC+LavG5hGcGpQks4tbmu8j2mMaWujnKMdapVi2nFJpKS4OTNvBdTpNH2/KDj7pNFb4gtHK/uVuXTSefi8/eBj0rpSviCrrVHsXZis9SC5cz7oUVRWS9r7z6pU1SWSX+97PsAZrOg7mpCC3ykl8TCd/BVr091rPdTi5e17EBPaUFTiorckkvYfYAAAAAAAAAAAAADh4w0t/xNpOUX95PqQ8XvfsQEPx5iN3k3b0n91B5VGv+yfd4Ihx63mewg6jSim23kks228wPIpyeS2t7Elx5eJY2DcI/ZNWvcrOpvhTe6nzl3y8jNg7CS0clWrpOs9sY7GqX1l5G1i3FENDRcKeUrhrYt6pr1pfQDLirE1PQkNWOUq8l1YcI/ml9Cqbu6qXlSVSpJynJ5tvy8D5uK87mcpzk5Tk85Se1tmMAAbNpauttfZ8+SAs/wBHk9fR8Pyzmv8ALP5kbxXDUvavNxl/iiR4CaVrKK/DVfkjiY2hq3bffTi/NAcEAACcYFtejozqPfOWS8EQiMXJpLe3ki09F2v2OhTh6sEn48QNsAAAAAAAAAAAAAKv9I+kPtN0qSfVpR2/qe1/ItAr3EmCa9apUrUpqo5ycnB9WW3gnuYEHo0pVpKMU5Sk8klm22WfhDCkdFJVayUq7Wxb1S5LnzMuEsLQ0NFVKmUrhra96pr1Y/U1cYYtWjk6NBp1nslLeqX1l5AZsX4rjopOlRalXa28VSXe+fIq+tVlXk5TblKTzk3m22eTm6jbk223m2822z5AAG5Z2mvtlu4LvA8s7XpNr7Pn+x0ksgth6BM8ATzhXXdKL+D+hpY9hlXpvvpZe6T+plwBPr1l+WL+LPvH8NtCXKa8gIiAAOvhay+2XUM+zDry9m74lkEbwTY9BQdRrrVHs/SiSAAAAAAAAAAAAAAGlpi8dhb1aqyzhByWe7PgcXC+LYaafRziqdbLNLPOM1xy58jPjup0ejq3PVj75IqmxuJWlWnUi8pQmpL2Pd/veBbWMbqvZWdSdDJSWSlLjGD2OS5lPyk5PN7W3m2+JedzRjfUZQl2alNxfhJEFufRzNfy7iL5Si4/FZgQUElucD39HdCE/wBMo/PI1KeHrmg86tGokuGTft2AaVnaa3Wlu4Lv5s6O49cXHesjwAAAJJgSerczXfSfwkjo4+hnSovuqNe+P7HGwZPVvI84TXwJDjmGtap91WPkwIEbFhau9qwpx3ykl4LizXJjgfRuqpV5Lf1YeHFgSq3oqhCMY7opJewyAAAAAAAAAAAAAAAEY9Iry0fLnUh5srzDui56WuadOKerrKU3wjBb/wDeZbml9F09L0ujq62prKXVeq81zPLDR9voWm1TjGnBLOUnvfOUnvAaZv1oq2qVdnUh1U+Mt0V7yH23pH/qW/thL5NHLxviVaWkqVJ/cweef9SW3b+k4Nla6/Wlu4Lv/YCzbLGdrcpNqpDP1ln5HUoabta/ZrQ9r1fMrDcALXlSo3S2qnNeEZGlXw7aVt9GKffHOPkVvTqSp9mTXg2jeoabuqHZrT8G9ZfECVV8G28+zOpH3SRz6+Cqi7FWL/UnH6mrQxfdU+10c/FZP4Es0BpKWlKPSSgo9ZxWTzzy4gaWg8NQ0a41Jycqq7tkI+Hede/sqd/TcKibi8nseTzI/ivT07KXRUXlPLOcuMc9yWfEj1jp67ozWVSU82upLrKW3dyA6d5hCcKsFTlrUpSybfagufeTK2oxtoRhFZRikke0pOcYuS1W0m1vyfcZAAAAAAAAAAAAAAAAAORiq9qaOs6tSk0px1cm0nvkkVTpLTVzpP8AnVZyXq7FH3LYWH6RrlUbLU41KkUvBbX5Fa2lt0zzfZW/nyA+rK26Xa+z5/sdJLIJaq2bj0AAAAAAFhYMmpWcUuE5p+/P5lekxwRCvQ11KElSl1lJ7Mpclz+QHIxZQlG9nsb19Vx5rLI72F8PfZMqtZfefhj6nPxJDUt4VJRnKMXKOerJrbHwMwAAAAAAAAAAAAAAAAAAAcPFGH46dppazjUhm4PhzTRFrDCdzVzTiqcYvLOXHwy3ligCGfwTL+sv7WfMsFVOFaHuZNQBBpYLrrdUpv8AuXyMf8HXPrU/e/oT0AQWGDK731Ka/ufyN62wXCP8yrJ8opLzJYAObZaDtrLbCms/Wl1pHSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/Z", "alta.png")
col1, col2 = st.columns([1,1])
image = Image.open("alta.png")
now = datetime.now()
date_heure = now.strftime("%d/%m/%Y %H:%M:%S")
date = now.strftime("%d/%m/%Y")
heure = now.strftime("%H:%M:%S")
st.text("Date et heure : " + date_heure)

with col1:
    st.title("Simulateur CO2")
    st.title("Altaroad")
with col2:
    st.image(image)

FEterres = 4.58
FEgravats = 12
FEdnd = 84
FEdd = 128
FEmoy5e = 0.0711/1000
FEmoy4e = 0.105/1000
mav5e = 15
mav4e = 12
prix_c = 2
prix_ISDI1 = 300
prix_ISDI2 = 300
prix_ISDND = 600
prix_ISDD = 1500
conso_moy = 30 / 100

col1, col2 = st.columns(2)
with col1:
    st.header("Quantité de déchets à évacuer")

    ISDI1brut = st.number_input("Terres à excaver (en tonnes)", step=1)
    ISDI2 = st.number_input("Déchets inertes : Gravats (en tonnes)", step=1)
    ISDND = st.number_input("Déchets non-dangereux en mélange (en tonnes)", step=1)
    ISDD = st.number_input("Déchets dangereux (en tonnes)", step=1)

with col2:
    st.header("Distance chantier-exutoire")

    dist_exuISDI1 = st.number_input("Distance exutoire 1 (en km)", value=35, step=1)
    dist_exuISDI2 = st.number_input("Distance exutoire 2 (en km)", value=35, step=1)
    dist_exuISDND = st.number_input("Distance exutoire 3 (en km)", value=35, step=1)
    dist_exuISDD = st.number_input("Distance exutoire 4 (en km)", value=35, step=1)

col1, col2 = st.columns(2)
with col1:
    st.header("Nombre de passages quotidiens")
    pass_jour = st.slider("Nombre de passages quotidien estimés",10,100,50, step=1)

with col2:
    st.header("Taux de réemploi des terres :")
    repl_terres = st.slider("Réemploi des terres sur site (%)",0,100,0, step=1)
    valo_terres = 100 - repl_terres
    # st.slider("Envoi vers exutoire pour valorisation (%)",0,100,100, step=1)
    ISDI1 = math.ceil(ISDI1brut * (valo_terres/100))

col1, col2 = st.columns(2)
with col1:
    st.header("Type de camions")
    nb_cam5 = st.number_input("Nombre de camions 5 essieux articulés", value=20, step=1)
    nb_cam4 = st.number_input("Nombre de camions 4 essieux porteurs", value=10, step=1)
    cam5 = (nb_cam5 / (nb_cam5 + nb_cam4)) * 100
    cam4 = (nb_cam4 / (nb_cam5 + nb_cam4)) * 100
with col2:
    st.header("Chargement moyen")
    load_cam5 = st.slider("Chargement moyen des camions articulés (tonnes)",15,29,25, step=1)
    load_cam4 = st.slider("Chargement moyen des camions porteurs (tonnes)",10,20,15, step=1)

pass_ISDI1 = math.ceil(ISDI1/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDI2 = math.ceil(ISDI2/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDND = math.ceil(ISDND/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDD = math.ceil(ISDD/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_tot = pass_ISDI1+pass_ISDI2+pass_ISDND+pass_ISDD
FE_trans = FEmoy5e*(cam5/100)+FEmoy4e*(cam4/100)
tot_D = ISDI1+ISDI2+ISDND+ISDD
dist_tot = pass_ISDI1*dist_exuISDI1 + pass_ISDI2*dist_exuISDI2 + pass_ISDND*dist_exuISDND + pass_ISDD*dist_exuISDD

st.header("Données & Bilan CO2e")
E_ISDI1 = round((ISDI1*FEterres)/1000, 1)
E_ISDI2 = round((ISDI2*FEgravats)/1000, 1)
E_ISDND = round((ISDND*FEdnd)/1000, 1)
E_ISDD = round((ISDD*FEdd)/1000, 1)
E_trans_ISDI1 = round(FE_trans * dist_exuISDI1 * (ISDI1 + mav5e * (cam5/100) * pass_ISDI1 + mav4e * (cam4/100) * pass_ISDI1), 0)
E_trans_ISDI2 = round(FE_trans * dist_exuISDI2 * (ISDI2 + mav5e * (cam5/100) * pass_ISDI2 + mav4e * (cam4/100) * pass_ISDI2), 0)
E_trans_ISDND = round(FE_trans * dist_exuISDND * (ISDND + mav5e * (cam5/100) * pass_ISDND + mav4e * (cam4/100) * pass_ISDND), 0)
E_trans_ISDD = round(FE_trans * dist_exuISDD * (ISDD + mav5e * (cam5/100) * pass_ISDD + mav4e * (cam4/100) * pass_ISDD), 0)
E_trans = FE_trans * (dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
                      + dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
                      + dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
                      + dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD))

E_valo = E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD
E_tot = E_trans + E_valo
with st.expander("Emissions de CO2e par types de déchets :"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Terres")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(int(E_ISDI1))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDI1))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDI1+E_trans_ISDI1))
        if ISDI1 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDI1 + E_trans_ISDI1)/ISDI1)*1000))
    with col2:
        st.subheader("Gravats")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(int(E_ISDI2))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDI2))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDI2 + E_trans_ISDI2))
        if ISDI2 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDI2 + E_trans_ISDI2)/ISDI2)*1000))
    with col3:
        st.subheader("DND")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(int(E_ISDND))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDND))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDND + E_trans_ISDND))
        if ISDND > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDND + E_trans_ISDND)/ISDND)*1000))
    with col4:
        st.subheader("DD")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(int(E_ISDD))
        st.write("CO2e transport (en tCO2e):")
        st.subheader(int(E_trans_ISDD))
        st.write("CO2e total (en tCO2e):")
        st.subheader(int(E_ISDD + E_trans_ISDD))
        if ISDD > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_ISDD + E_trans_ISDD)/ISDD)*1000))

with st.expander("Emissions totales de CO2e (en tCO2e):"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Transport :")
        st.subheader(int(E_trans))
    with col2:
        st.write("Valorisation :")
        st.subheader(int(E_valo))
    with col3:
        st.write("Total des émissions :")
        st.subheader(int(E_tot))
    with col4:
        if tot_D > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(int(((E_trans+E_valo)/tot_D)*1000))

with st.expander("Distance à parcourir :"):
    st.subheader(str(dist_tot) + " km")

with st.expander("Passages :"):
    st.write("Total passages :")
    st.subheader(pass_tot)
    st.write("Total jours évacuation :")
    jours_evacuation = math.ceil(pass_tot/pass_jour)
    st.subheader(jours_evacuation)
    st.write("Nombre de passages pour l'évacuation des terres :")
    st.subheader(pass_ISDI1)
    st.write("Nombre de passages pour l'évacuation des gravats :")
    st.subheader(pass_ISDI2)
    st.write("Nombre de passages pour l'évacuation des déchets non-dangereux :")
    st.subheader(pass_ISDND)
    st.write("Nombre de passages pour l'évacuation des dangereux :")
    st.subheader(pass_ISDD)

st.header("Actions de réduction et gains")

#Réutiliser 10% des terres sur site
action1 = st.checkbox('Augmenter de 10% la réutilisation des terres sur site')
new_valo_terres = valo_terres - 10
new_ISDI1 = ISDI1brut * (new_valo_terres/100)
new_E_ISDI1 = (new_ISDI1 * FEterres)/1000
new_pass_ISDI1 = math.ceil(new_ISDI1/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
new_E_trans_ISDI1 = FE_trans * dist_exuISDI1 * (new_ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1 + mav4e * (cam4 / 100) * new_pass_ISDI1)
new_pass_tot = new_pass_ISDI1 + pass_ISDI2 + pass_ISDND + pass_ISDD
Ea1 = E_ISDI1+E_trans_ISDI1-new_E_ISDI1-new_E_trans_ISDI1
conso_tot_Ea1 = conso_moy * pass_tot * dist_exuISDI1
new_conso_tot_Ea1 = conso_moy * new_pass_tot * dist_exuISDI1
eco_c_Ea1 = (conso_tot_Ea1 - new_conso_tot_Ea1) * prix_c
eco_ISDI = (pass_ISDI1 - new_pass_ISDI1) * prix_ISDI1
if action1:
    if valo_terres >= 10:
        v = random.choice([str(math.ceil(Ea1 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea1 * 5181)) + " km en voiture (" + str(math.ceil(Ea1 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea1)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea1 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea1 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea1 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea1 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea1)) + " tCO2e, soit " + str(int((Ea1/E_tot)*100)) + " % des émissions totales estimées")
            st.write("soit " + v)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de (évacuation des terres) :")
            st.subheader(str(pass_ISDI1-new_pass_ISDI1) + " passages, " + str(math.ceil(jours_evacuation - (new_pass_tot / pass_jour))) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea1)) + " €")
            st.write("Gain € évacuation terres : ")
            st.subheader(str(math.ceil(eco_ISDI)) + " €")
    else:
        st.error("Le taux de réutilisation des terres sur site est déjà supérieur à 90%")

#Privilégier les camions 5 essieux (de 70% à 80%)
action2 = st.checkbox("Utiliser 15% de camions 5 essieux en plus")
new_cam5 = cam5 + 15
new_cam4 = 100 - new_cam5
new_FE_trans = FEmoy5e * (new_cam5 / 100) + FEmoy4e * (new_cam4 / 100)
new_E_trans_ISDI1_Ea2 = round(new_FE_trans * dist_exuISDI1 * (ISDI1 + mav5e * (new_cam5 / 100) * pass_ISDI1 + mav4e * (new_cam4 / 100) * pass_ISDI1), 1)
new_E_trans_ISDI2_Ea2 = round(new_FE_trans * dist_exuISDI2 * (ISDI2 + mav5e * (new_cam5 / 100) * pass_ISDI2 + mav4e * (new_cam4 / 100) * pass_ISDI2), 1)
new_E_trans_ISDND_Ea2 = round(new_FE_trans * dist_exuISDND * (ISDND + mav5e * (new_cam5 / 100) * pass_ISDND + mav4e * (new_cam4 / 100) * pass_ISDND), 1)
new_E_trans_ISDD_Ea2 = round(new_FE_trans * dist_exuISDD * (ISDD + mav5e * (new_cam5 / 100) * pass_ISDD + mav4e * (new_cam4 / 100) * pass_ISDD), 1)
new_pass_ISDI1_Ea2 = math.ceil(ISDI1 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDI2_Ea2 = math.ceil(ISDI2 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDND_Ea2 = math.ceil(ISDND / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_ISDD_Ea2 = math.ceil(ISDD / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
new_pass_tot_Ea2 = new_pass_ISDI1_Ea2 + new_pass_ISDI2_Ea2 + new_pass_ISDND_Ea2 + new_pass_ISDD_Ea2
new_E_trans_Ea2 = new_FE_trans * (dist_exuISDI1 * (ISDI1 + mav5e * (new_cam5 / 100) * new_pass_ISDI1_Ea2 + mav4e * (new_cam4 / 100) * new_pass_ISDI1_Ea2)
                              + dist_exuISDI2 * (ISDI2 + mav5e * (new_cam5 / 100) * new_pass_ISDI2_Ea2 + mav4e * (new_cam4 / 100) * new_pass_ISDI2_Ea2)
                              + dist_exuISDND * (ISDND + mav5e * (new_cam5 / 100) * new_pass_ISDND_Ea2 + mav4e * (new_cam4 / 100) * new_pass_ISDND_Ea2)
                              + dist_exuISDD * (ISDD + mav5e * (new_cam5 / 100) * new_pass_ISDD_Ea2 + mav4e * (new_cam4 / 100) * new_pass_ISDD_Ea2))
Ea2 = round(E_trans - new_E_trans_Ea2, 1)
conso_tot = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea2 = (conso_moy * new_pass_ISDI2_Ea2 * dist_exuISDI2) + (conso_moy * new_pass_ISDI1_Ea2 * dist_exuISDI1) + (conso_moy * new_pass_ISDND_Ea2 * dist_exuISDND) + (conso_moy * new_pass_ISDD_Ea2 * dist_exuISDD)
eco_c_Ea2 = (conso_tot - new_conso_tot_Ea2) * prix_c
eco_ISDI1_Ea2 = (pass_ISDI1 - new_pass_ISDI1_Ea2) * prix_ISDI1
eco_ISDI2_Ea2 = (pass_ISDI2 - new_pass_ISDI2_Ea2) * prix_ISDI2
eco_ISDND_Ea2 = (pass_ISDND - new_pass_ISDND_Ea2) * prix_ISDND
eco_ISDD_Ea2 = (pass_ISDD - new_pass_ISDD_Ea2) * prix_ISDD
eco_D_tot_Ea2 = eco_ISDI1_Ea2 + eco_ISDI2_Ea2 + eco_ISDND_Ea2 + eco_ISDD_Ea2
if action2:
    if cam5 <= 85:
        w = random.choice([str(math.ceil(Ea2*138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea2*5181)) + " km en voiture (" + str(math.ceil(Ea2 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea2)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea2*54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea2*61)) + " smartphones 📱",
                           str(math.ceil(Ea2*2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea2*43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea2)) + " tCO2e, soit " + str(int((Ea2/E_tot)*100)) + " % des émissions totales estimées")
            st.write("soit " + w)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(pass_tot - new_pass_tot_Ea2) + " passages, " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea2 / pass_jour))) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea2)) + " €")
            st.write("Gain € évacuations : ")
            st.subheader(str(math.ceil(eco_D_tot_Ea2)) + " €")
    else:
        st.error("Le taux d'utilisation de 5 essieux est déjà supérieur à 85%")

#Optimiser le chargement de 2 tonnes (borner l'action)
action3 = st.checkbox('Optimiser le chargement moyen des camions de 2 tonnes')
new_load_cam5 = load_cam5 + 2
new_load_cam4 = load_cam4 + 2
new_pass_ISDI1_Ea3 = math.ceil(ISDI1 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDI2_Ea3 = math.ceil(ISDI2 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDND_Ea3 = math.ceil(ISDND / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_ISDD_Ea3 = math.ceil(ISDD / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
new_pass_tot_Ea3 = new_pass_ISDI1_Ea3 + new_pass_ISDI2_Ea3 + new_pass_ISDND_Ea3 + new_pass_ISDD_Ea3
new_E_trans_Ea3 = FE_trans * (dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1_Ea3 + mav4e * (cam4 / 100) * new_pass_ISDI1_Ea3)
            + dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * new_pass_ISDI2_Ea3 + mav4e * (cam4 / 100) * new_pass_ISDI2_Ea3)
            + dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * new_pass_ISDND_Ea3 + mav4e * (cam4 / 100) * new_pass_ISDND_Ea3)
            + dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * new_pass_ISDD_Ea3 + mav4e * (cam4 / 100) * new_pass_ISDD_Ea3))
Ea3 = E_trans - new_E_trans_Ea3
conso_tot_Ea3 = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea3 = (conso_moy * new_pass_ISDI2_Ea3 * dist_exuISDI2) + (conso_moy * new_pass_ISDI1_Ea3 * dist_exuISDI1) + (conso_moy * new_pass_ISDND_Ea3 * dist_exuISDND) + (conso_moy * new_pass_ISDD_Ea3 * dist_exuISDD)
eco_c_Ea3 = (conso_tot - new_conso_tot_Ea3) * prix_c
eco_ISDI1_Ea3 = (pass_ISDI1 - new_pass_ISDI1_Ea3) * prix_ISDI1
eco_ISDI2_Ea3 = (pass_ISDI2 - new_pass_ISDI2_Ea3) * prix_ISDI2
eco_ISDND_Ea3 = (pass_ISDND - new_pass_ISDND_Ea3) * prix_ISDND
eco_ISDD_Ea3 = (pass_ISDD - new_pass_ISDD_Ea3) * prix_ISDD
eco_D_tot_Ea3 = eco_ISDI1_Ea3 + eco_ISDI2_Ea3 + eco_ISDND_Ea3 + eco_ISDD_Ea3
if action3:
    if load_cam4 <= 18 and load_cam5 <= 27:
        x = random.choice([str(math.ceil(Ea3 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea3 * 5181)) + " km en voiture (" + str(math.ceil(Ea3 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea3)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea3 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea3 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea3 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea3 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea3)) + " tCO2e, soit " + str(int((Ea3 / E_tot) * 100)) + " % des émissions totales estimées")
            st.write("soit " + x)
        with st.expander("Réduction du nombre de passages"):
            st.write("Cette action permet de réduire le nombre de passages de :")
            st.subheader(str(pass_tot - new_pass_tot_Ea3) + " passages, " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea3 / pass_jour))) + " jours")
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea3)) + " €")
            st.write("Gain € évacuations : ")
            st.subheader(str(math.ceil(eco_D_tot_Ea3)) + " €")
    else:
        st.error("Le chargement maximal est dépassé")

#Choix d'un exutoire 10 km plus proche
action4 = st.checkbox("Choisir un exutoire 10 km plus proche")
new_dist_exuISDI1 = dist_exuISDI1 - 10
new_dist_exuISDI2 = dist_exuISDI1 - 10
new_dist_exuISDND = dist_exuISDI1 - 10
new_dist_exuISDD = dist_exuISDI1 - 10
new_E_trans_Ea4 = FE_trans * (new_dist_exuISDI1 * (ISDI1 + mav5e * (cam5 / 100) * pass_ISDI1 + mav4e * (cam4 / 100) * pass_ISDI1)
            + new_dist_exuISDI2 * (ISDI2 + mav5e * (cam5 / 100) * pass_ISDI2 + mav4e * (cam4 / 100) * pass_ISDI2)
            + new_dist_exuISDND * (ISDND + mav5e * (cam5 / 100) * pass_ISDND + mav4e * (cam4 / 100) * pass_ISDND)
            + new_dist_exuISDD * (ISDD + mav5e * (cam5 / 100) * pass_ISDD + mav4e * (cam4 / 100) * pass_ISDD))
Ea4 = E_trans - new_E_trans_Ea4
conso_tot__Ea4 = (conso_moy * pass_ISDI2 * dist_exuISDI2) + (conso_moy * pass_ISDI1 * dist_exuISDI1) + (conso_moy * pass_ISDND * dist_exuISDND) + (conso_moy * pass_ISDD * dist_exuISDD)
new_conso_tot_Ea4 = (conso_moy * pass_ISDI2 * new_dist_exuISDI2) + (conso_moy * pass_ISDI1 * new_dist_exuISDI1) + (conso_moy * pass_ISDND * new_dist_exuISDND) + (conso_moy * pass_ISDD * new_dist_exuISDD)
eco_c_Ea4 = (conso_tot - new_conso_tot_Ea4) * prix_c
if action4:
    if dist_exuISDI1 >= 10 and dist_exuISDI2 >= 10 and dist_exuISDND >= 10 and dist_exuISDD >= 10:
        y = random.choice([str(math.ceil(Ea4 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea4 * 5181)) + " km en voiture (" + str(math.ceil(Ea4 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea4)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea4 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea4 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea4 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea4 * 43)) + " jeans en coton 👖"])
        with st.expander("Réduction des émissions carbone"):
            st.write("Cette action permet de réduire les émissions totales de :")
            st.subheader(str(int(Ea4)) + " tCO2e, soit " + str(int((Ea4/E_tot)*100)) + " % des émissions totales estimées")
            st.write("soit " + y)
        with st.expander("Estimation du gain économique €"):
            st.write("Gain € carburant : ")
            st.subheader(str(math.ceil(eco_c_Ea4)) + " €")
    else:
        st.error("Un des exutoires se trouve déjà à moins de 10 km du chantier")

#Toutes les actions combinées
action5 = st.checkbox("Combiner toutes les actions de réduction")
new_pass_ISDI1_Ea5 = math.ceil(new_ISDI1 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDI2_Ea5 = math.ceil(ISDI2 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDND_Ea5 = math.ceil(ISDND / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_pass_ISDD_Ea5 = math.ceil(ISDD / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
new_E_trans_Ea5 = FE_trans * (new_dist_exuISDI1 * (ISDI1 + mav5e * (new_cam5 / 100) * new_pass_ISDI1_Ea5 + mav4e * (new_cam4 / 100) * new_pass_ISDI1_Ea5)
                          + new_dist_exuISDI2 * (ISDI2 + mav5e * (new_cam5 / 100) * new_pass_ISDI2_Ea5 + mav4e * (new_cam4 / 100) * new_pass_ISDI2_Ea5)
                          + new_dist_exuISDND * (ISDND + mav5e * (new_cam5 / 100) * new_pass_ISDND_Ea5 + mav4e * (new_cam4 / 100) * new_pass_ISDND_Ea5)
                          + new_dist_exuISDD * (ISDD + mav5e * (new_cam5 / 100) * new_pass_ISDD_Ea5 + mav4e * (new_cam4 / 100) * new_pass_ISDD_Ea5))
new_tot_D = new_ISDI1 + ISDI2 + ISDND + ISDD
new_pass_tot_Ea5 = new_pass_ISDI1_Ea5 + new_pass_ISDI2_Ea5 + new_pass_ISDND_Ea5 + new_pass_ISDD_Ea5
new_E_valo = round(new_E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD, 1)
new_E_tot_Ea5 = new_E_trans_Ea5 + new_E_valo
Ea5 = E_tot - new_E_tot_Ea5
new_conso_tot_Ea5 = (conso_moy * new_pass_ISDI2_Ea5 * new_dist_exuISDI2) + (conso_moy * new_pass_ISDI1_Ea5 * new_dist_exuISDI1) + (conso_moy * new_pass_ISDND_Ea5 * new_dist_exuISDND) + (conso_moy * new_pass_ISDD_Ea5 * new_dist_exuISDD)
eco_c_Ea5 = (conso_tot - new_conso_tot_Ea5) * prix_c
eco_ISDI1_Ea5 = (pass_ISDI1 - new_pass_ISDI1_Ea5) * prix_ISDI1
eco_ISDI2_Ea5 = (pass_ISDI2 - new_pass_ISDI2_Ea5) * prix_ISDI2
eco_ISDND_Ea5 = (pass_ISDND - new_pass_ISDND_Ea5) * prix_ISDND
eco_ISDD_Ea5 = (pass_ISDD - new_pass_ISDD_Ea5) * prix_ISDD
eco_D_tot_Ea5 = eco_ISDI1_Ea5 + eco_ISDI2_Ea5 + eco_ISDND_Ea5 + eco_ISDD_Ea5
if action5:
    z = random.choice([str(math.ceil(Ea5 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea5 * 5181)) + " km en voiture (" + str(math.ceil(Ea5 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea5)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea5 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea5 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea5 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea5 * 43)) + " jeans en coton 👖"])
    with st.expander("Réduction des émissions carbone"):
        st.write("Cette action permet de réduire les émissions totales de :")
        st.subheader(str(int(Ea5)) + " tCO2e, soit " + str(int((Ea5 / E_tot) * 100)) + " % des émissions totales estimées")
        st.write("soit " + z)
    with st.expander("Réduction du nombre de passages"):
        st.write("Cette action permet de réduire le nombre de passages de :")
        st.subheader(str(pass_tot - new_pass_tot_Ea5) + " passages, " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea5 / pass_jour))) + " jours")
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
st.caption("- Coût d'évacuation d'un chargement 'déchets non-dangereux' : 600 €")
st.caption("- Coût d'évacuation d'un chargement 'déchets dangereux' : 1500 €")

st.header("Estimation du bilan CO2 de la construction de l'ouvrage")
st.caption("Données issue de la Base Carbone® de l'ADEME")
bdd = "data_FE_ouvrages.csv"
df = pd.read_csv(bdd, encoding="latin1", sep=";", decimal=',')
df["Type d'ouvrage"] = df["Type d'ouvrage"].astype(str)
df["Catégorie"] = df["Catégorie"].astype(str)
df["Sous catégorie 1"] = df["Sous catégorie 1"].astype(str)
df["Sous catégorie 2"] = df["Sous catégorie 2"].astype(str)
df["Unité"] = df["Unité"].astype(str)

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
DO = float(st.number_input("Donnée opérationnelle (en " + u + ") : ", step=1))
for x in df["FE"]:
    x = float(x)
for i in df["Incertitude"]:
    i = float(i)
EMISSIONS = round(x / 1000 * DO, 2)
INCERTITUDE = round(EMISSIONS * 0.01 * i, 2)
st.write(" ")

st.subheader("Emissions GES de l'ouvrage 💨 : " + str(int(EMISSIONS)) + " tCO2e ")
st.write("(+ ou - " + str(int(INCERTITUDE)) + " tCO2e)")

st.header("Graphiques")
with st.expander("Déchets"):
    col1, col2 = st.columns(2)
    with col1:
        labels = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
        sizes = [ISDI1, ISDI2, ISDND, ISDD]
        fig1, ax1 = plt.subplots()
        ax1.set_title("Part des déchets par 'type'")
        ax1.pie(sizes, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.legend(labels, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig1)

        labels2 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
        sizes2 = [E_ISDI1, E_ISDI2, E_ISDND, E_ISDD]
        fig2, ax2 = plt.subplots()
        ax2.set_title("Emissions de CO2 par déchet : valorisation")
        ax2.pie(sizes2, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        ax2.legend(labels2, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig2)

        labels3 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
        sizes3 = [E_trans_ISDI1, E_trans_ISDI2, E_trans_ISDND, E_trans_ISDD]
        fig3, ax3 = plt.subplots()
        ax3.set_title("Emissions de CO2e par déchet : transport")
        ax3.pie(sizes3, autopct='%1.1f%%', startangle=90)
        ax3.axis('equal')
        ax3.legend(labels3, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig3)
    with col2:
        labels4 = 'Terres', 'Gravats', 'Déchets Non-Dangereux', 'Déchets Dangereux'
        sizes4 = [E_ISDI1+E_trans_ISDI1, E_ISDI2+E_trans_ISDI2, E_ISDND+E_trans_ISDND, E_ISDD+E_trans_ISDD]
        fig4, ax4 = plt.subplots()
        ax4.set_title("Emissions CO2e globales par déchet")
        ax4.pie(sizes4, autopct='%1.1f%%', startangle=90)
        ax4.axis('equal')
        ax4.legend(labels4, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig4)

        labels5 = 'Valorisation', 'Transport'
        sizes5 = [E_valo, E_trans]
        fig5, ax5 = plt.subplots()
        ax5.set_title("Part des émissions de CO2e Valorisation/Transport")
        ax5.pie(sizes5, autopct='%1.1f%%', startangle=90)
        ax5.axis('equal')
        ax5.legend(labels5, title="Déchets", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig5)

with st.expander("Réductions"):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    actions = ["+ 10% de terres réutilisées", "+ 15% de camions 5 essieux", "+ 2t de chargement moyen", "- 10km distance chantier/exutoire", "Toutes les actions"]
    valeurs = [Ea1, Ea2, Ea3, Ea4, Ea5]
    ax.set_title('Diminution des émissions CO2e par action')
    ax.set_ylabel('tCO2e')
    ax.set_xlabel('Actions de réduction')
    plt.xticks(rotation=45)
    ax.bar(actions, valeurs, color='grey', edgecolor='orange')
    st.pyplot(fig)

st.header("Synthèse")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", size=22)
pdf.cell(200, 10, txt="Synthèse des résultats", ln=1, align='C')
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", size=8)
pdf.cell(200, 10, txt=date_heure, ln=1)
pdf.cell(200, 10, txt="", ln=2)

pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Données entrées",ln=4)
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Terres : " + str(ISDI1) + " tonnes, chantier > exutoire : " + str(dist_exuISDI1) + " km", ln=5)
pdf.cell(200, 10, txt="Gravats : " + str(ISDI2) + " tonnes, chantier > exutoire : " + str(dist_exuISDI2) + " km", ln=6)
pdf.cell(200, 10, txt="Déchets non-dangereux : " + str(ISDND) + " tonnes, chantier > exutoire : " + str(dist_exuISDND) + " km", ln=7)
pdf.cell(200, 10, txt="Déchets dangereux : " + str(ISDD) + " tonnes, chantier > exutoire : " + str(dist_exuISDD) + " km", ln=8)
pdf.cell(200, 10, txt="Nombre de passages quotidien : " + str(pass_jour), ln=9)
pdf.cell(200, 10, txt="Taux de réemploi des terres : " + str(repl_terres) + "%", ln=10)
pdf.cell(200, 10, txt="Camions : 5 essieux articulés : " + str(nb_cam5) + " soit " + str(int(cam5)) + " % ,4 essieux porteurs : " + str(nb_cam4) + " soit " + str(int(cam4)) + " %", ln=11)
pdf.cell(200, 10, txt="Chargement moyen des 5 essieux : " + str(load_cam5) + " ,chargement moyen des 4 essieux : " + str(load_cam4), ln=12)
pdf.cell(200, 10, txt="", ln=2)

pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Données de sortie",ln=4)
pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Distance totale à parcourir : " + str(int(dist_tot)) + " km", ln=3)
pdf.cell(200, 10, txt="Nombre total de passages : " + str(int(pass_tot)), ln=3)
pdf.cell(200, 10, txt="Nombre de jours d'évacuation : " + str(int(jours_evacuation)), ln=3)

pdf.add_page()
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Bilan CO2e",ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Emissions CO2e totales estimées : " + str(int(E_tot)) + " tCO2e", ln=3)
if E_tot>0:
    pdf.cell(200, 10, txt="Emissions CO2e totales 'Transport' : " + str(int(E_trans)) + " tCO2e, soit " + str(int((E_trans/E_tot)*100)) + " %", ln=3)
    pdf.cell(200, 10, txt="Emissions CO2e totales 'Valorisation' : " + str(int(E_valo)) + " tCO2e, soit " + str(int((E_valo/E_tot)*100)) + " %", ln=3)
pdf.cell(200, 10, txt="", ln=2)
pdf.cell(200, 10, txt="Emissions CO2e 'Terres' : "  "Transport = "+ str(int(E_trans_ISDI1)) + " tCO2e; Valorisation = " + str(int(E_ISDI1)) + " tCO2e; Total = " + str(int(E_ISDI1 + E_trans_ISDI1)) + " tCO2e", ln=3)
pdf.cell(200, 10, txt="Emissions CO2e 'Gravats' : "  "Transport = "+ str(int(E_trans_ISDI2)) + " tCO2e; Valorisation = " + str(int(E_ISDI2)) + " tCO2e; Total = " + str(int(E_ISDI2 + E_trans_ISDI2)) + " tCO2e", ln=3)
pdf.cell(200, 10, txt="Emissions CO2e 'DND' : "  "Transport = "+ str(int(E_trans_ISDND)) + " tCO2e; Valorisation = " + str(int(E_ISDND)) + " tCO2e; Total = " + str(int(E_ISDND + E_trans_ISDND)) + " tCO2e", ln=3)
pdf.cell(200, 10, txt="Emissions CO2e 'DD' : "  "Transport = "+ str(int(E_trans_ISDD)) + " tCO2e; Valorisation = " + str(int(E_ISDD)) + " tCO2e; Total = " + str(int(E_ISDD + E_trans_ISDD)) + " tCO2e", ln=3)

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Actions de réduction et gains",ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="+ 10% de réutilisation des terres sur site : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea1)) + " tCO2e; Gain passages = " + str(int(pass_ISDI1-new_pass_ISDI1)) + " soit " + str(math.ceil(jours_evacuation - (new_pass_tot / pass_jour))) + " jours; Gain économique = " + str(math.ceil(eco_c_Ea1 + eco_ISDI)) + " euros", ln=3)
pdf.cell(200, 10, txt="+ 15% de camions 5 essieux articulés : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea2)) + " tCO2e; Gain passages = " + str(int(pass_tot-new_pass_tot_Ea2)) + " soit " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea2 / pass_jour))) + " jours; Gain économique = " + str(math.ceil(eco_c_Ea2 + eco_D_tot_Ea2)) + " euros", ln=3)
pdf.cell(200, 10, txt="+ 2 tonnes de chargement moyen : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea3)) + " tCO2e; Gain passages = " + str(int(pass_tot-new_pass_tot_Ea3)) + " soit " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea3 / pass_jour))) + " jours; Gain économique = " + str(math.ceil(eco_c_Ea3 + eco_D_tot_Ea3)) + " euros", ln=3)
pdf.cell(200, 10, txt="- 10 km de distance à l'exutoire : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea4)) + " tCO2e; Gain économique = " + str(math.ceil(eco_c_Ea4)) + " euros", ln=3)
pdf.cell(200, 10, txt="Toutes les actions de réductions combinées : ", ln=3)
pdf.cell(200, 10, txt="Gain CO2e = " + str(int(Ea5)) + " tCO2e; Gain passages = " + str(int(pass_tot-new_pass_tot_Ea5)) + " soit " + str(math.ceil(jours_evacuation - (new_pass_tot_Ea5 / pass_jour))) + " jours; Gain économique = " + str(math.ceil(eco_c_Ea5 + eco_D_tot_Ea5)) + " euros", ln=3)

pdf.cell(200, 10, txt="", ln=2)
pdf.set_font("Arial", "B", size=14)
pdf.cell(200, 10, txt="Estimation du bilan CO2 de la construction de l'ouvrage",ln=4)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Selon les données de l'ADEME, la construction de ce type d'ouvrage d'une surface de " + str(int(DO)) +  " m²,", ln=3)
pdf.cell(200, 10, txt="émetterait environ " + str(int(EMISSIONS)) + " tCO2e (+ ou - " + str(int(INCERTITUDE)) + " tCO2e).", ln=3)
pdf = pdf.output("SYNTHESE.pdf")
with open("SYNTHESE.pdf", "rb") as pdf_file:
   PDFbyte = pdf_file.read()
st.download_button(label="Télécharger",
                    data=PDFbyte,
                    file_name="SYNTHESE.pdf",
                    mime='application/octet-stream')
st.write("")
st.caption("""Les données sources utilisées sont référencées et disponible sur demande à Altaroad

Développé par Altaroad - CONFIDENTIEL 2022 - https://www.altaroad.com""")