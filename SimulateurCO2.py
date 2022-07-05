import pandas as pd
import streamlit as st
import numpy as np
import urllib.request
import math
import random
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

"""st.header("Choix du chantier et de l'exutoire")
gps_site={'l15_smc_C':[48.80676379609311, 2.4714128993643167],
          'l18_tcto_C':[48.71864217054404, 2.2267706822329747],
          'l18_mas_C':[48.72618364228579, 2.256979195965277],
          'X_austerlitz_C':[48.84101009097729, 2.3628191982951976],
          'X_e3s_C':[48.764337707431714, 2.2888278993623645],
          'l18_oa8_C':[48.73041281488208, 2.299016182160656],
          'l18_oa12_C':[48.73041281488208, 2.299016182160656],
          'l18_ant_C':[48.73614139875681, 2.3108366128519306],
          'X_t10_C':[48.77918448732479, 2.2521011398356183],
          'l15_chc_C':[48.818081419932184, 2.501509306150639]}
site = st.selectbox("Choix du site", gps_site)
coord1 = gps_site.get(site)
#Récupérer données chantier (nom, coord GPS (ou adresse))

gps_exu={'sgp_bonneuil_E':[48.78136128027323, 2.4867031109993354],
          'sgp_bruyere_oise_E':[49.150212134583846, 2.3367129821798214],
          'sgp_lagny_marne_E':[48.87634563470945, 2.678905695658136],
          'sgp_aulnay_bois_E':[48.95878248312839, 2.4855640282076026],
          'sgp_champagne_oise_E':[49.13540594986553, 2.2559238840337916],
          'ect_cormeilles_E':[48.9633919, 2.2143567],
          'ect_annet_E':[48.9321000, 2.72360083],
          'ect_auneuil_E':[49.3889375, 2.0036132],
          'ect_baillet_E':[49.0550194, 2.2890186],
          'ect_chelles_E':[48.892966, 2.5905579],
          'ect_chevannes_E':[48.536575, 2.422022],
          'ect_forges_E':[48.6008494, 2.0678437],
          'ect_grisy_suisnes_E':[48.686389, 2.697708],
          'ect_lacourneuve_E':[48.936929, 2.410814],
          'ect_lens_E':[50.432276, 2.845321],
          'ect_roissy_E':[48.783784, 2.626967],
          'ect_vaujours_E':[48.933681, 2.602302],
          'ect_villeneuve_E':[49.0310310, 2.6286292],
          'ect_villeparisis_E':[48.9356944, 2.6302777777777777],
          'lafarge_guerville_E':[48.96458006102009, 1.7570075975168304],
          'veolia_triel_E':[48.955341638668365, 2.0213898607531635],
          'cosson_puiseux_E':[49.06648191286999, 2.479039395666808],
          'veolia_claye_E':[48.94840582269361, 2.7203403686797096],
          'veolia_monthyon_E':[49.01744600518233, 2.8246193398464805],
          'bruyere_E':[49.15022616957621, 2.3367451686889606],
          'cemex_beauvilliers_E':[48.28941475198129, 1.7052754221049893],
          'cemex_saint-denis_E':[48.930756141419344, 2.341060311006168],
          'cemex_aubervilliers_E':[48.91471300358766, 2.3720397551873242],
          'cemex_point_jour_E':[48.836042403059494, 2.2634007263473697],
          'cemex_javel-haut_E':[48.854166954656975, 2.2812401817506722],
          'cemex_bercy_E':[48.84042470012778, 2.3761455696535783],
          'cemex_val_reuil_E':[49.28567504195899, 1.2348890128770635],
          'cemex_bouafles_E':[49.196967596969564, 1.374364784036617],
          'cemex_alizay_E':[49.316776332620485, 1.1667280300786589],
          'cemex_tolbiac_E':[48.83005670868657, 2.3832038938013804],
          'cemex_ivry_E':[48.825982162341525, 2.3882739398377715],
          'cemex_athis-mons_E':[48.70531414616078, 2.40059579935967],
          'cemex_evry_E':[48.62995307019293, 2.4605857263379787],
          'cemex_gennevilliers_E':[48.94253186996389, 2.2929529975158354],
          'cemex_marolles_E':[48.38750387725529, 3.0706238263269854],
          'cemex_pecy_E':[48.657621597499926, 3.0977914551756216],
          'gsm_acheres_E':[48.980997032566826, 2.0709067128631022],
          'ecoterres_bruyères_E':[49.14911670326355, 2.3306978551980446],
          'recycleo_villeau_E':[48.24708211596705, 1.5902035551570055],
          'brezillon_vitry_E':[48.78814167031243, 2.3616199975087695],
          'antrope_chevincourt_E':[49.52482912249918, 2.8439487705608233],
          'sita_laimont_E':[48.84351503969166, 5.031479797511305],
          'terralia_bourron_E':[48.34283222729696, 2.6766590398158256],
          'terralia_soucy_E':[48.24406404864583, 3.292801670502411],
          'coved_champigny_E':[48.30296448167418, 3.1230684551595185],
          'scbv_bannost_E':[48.6751796085341, 3.1728285705219346],
          'gsm_guerville_E':[48.96289768329372, 1.7389381840259135],
          'gsm_triel_E':[48.96222522257524, 2.008573600287507],
          'terralia_bray_E':[47.84305689633331, 2.3470011532841704],
          'brezillon_longueil_E':[49.316699932880844, 2.7247543245147106],
          'sita_villeparisis_E':[48.92933059540954, 2.603475770533497],
          'antrope_saintleudesserent_E':[49.225662629258075, 2.401051497528799],
          'extract_bruyere_sur_oise_E':[49.1491096856107, 2.3306978551980446],
          'not found':[48.893896731644446, 2.3541898956589606]}

exutoire = st.selectbox("Choix de l'exutoire", gps_exu)
coord2 = gps_exu.get(exutoire)

#map exutoire et site
df = pd.DataFrame([coord1, coord2], columns=['lat', 'lon'])
st.map(df)

#Appel openstreetmap? calul distance chantier/exutoire"""
st.header("Nombre de passages quotidien")

st.header("Quantité de déchets à évacuer")

ISDI1brut = st.number_input("Terres à excaver (en tonnes) : ", step=1)
ISDI2 = st.number_input("Déchets inertes : Gravats (en tonnes) : ", step=1)
ISDND = st.number_input("Déchets non-dangereux en mélange (en tonnes) :", step=1)
ISDD = st.number_input("Déchets dangereux (en tonnes) :", step=1)


st.header("Taux de valorisation / réemploi des terres :")
valo_terres = st.slider("Envoi vers exutoire pour valorisation (%)",0,100,100, step=1)
repl_terres = st.slider("Réemploi sur site (%)",0,100,100-valo_terres, step=1)
ISDI1 = ISDI1brut * (valo_terres/100)

st.header("Type de camions")
cam5 = st.slider("Pourcentage de camions 5 essieux (%)",0,100,70, step=1)
cam4 = st.slider("Pourcentage de camions 4 essieux (%)",0,100,100-cam5, step=1)

st.header("Chargement moyen")
load_cam5 = st.slider("Chargement moyen des camions 5 essieux (tonnes)",0,35,25, step=1)
load_cam4 = st.slider("Chargement moyen des camions 4 essieux (tonnes)",0,30,15, step=1)

pass_ISDI1 = math.ceil(ISDI1/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDI2 = math.ceil(ISDI2/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDND = math.ceil(ISDND/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_ISDD = math.ceil(ISDD/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
pass_tot = pass_ISDI1+pass_ISDI2+pass_ISDND+pass_ISDD
FE_trans = FEmoy5e*(cam5/100)+FEmoy4e*(cam4/100)
tot_D = ISDI1+ISDI2+ISDND+ISDD

st.header("Nombre de passages quotidien")
nb_passages = st.radio("", ('Faible (~10)', 'Moyen (~50)', 'Fort (~100)'))
if nb_passages == 'Faible (~10)':
    pass_jour = 10
elif nb_passages == 'Moyen (~50)':
    pass_jour = 50
elif nb_passages == 'Fort (~100)':
    pass_jour = 100

st.header("Données")

with st.expander("Distance à parcourir :"):
    st.subheader(str(dist_chantier_exutoire*pass_tot) + " km")

with st.expander("Passages :"):
    st.write("Nombre de passages pour l'évacuation des terres :")
    st.subheader(pass_ISDI1)
    st.write("Nombre de passages pour l'évacuation des gravats :")
    st.subheader(pass_ISDI2)
    st.write("Nombre de passages pour l'évacuation des déchets non-dangereux :")
    st.subheader(pass_ISDND)
    st.write("Nombre de passages pour l'évacuation des dangereux :")
    st.subheader(pass_ISDD)
    st.write("Total passages :")
    st.subheader(pass_tot)

st.header("Bilan CO2e")
E_ISDI1 = round((ISDI1*FEterres)/1000, 1)
E_ISDI2 = round((ISDI2*FEgravats)/1000, 1)
E_ISDND = round((ISDND*FEdnd)/1000, 1)
E_ISDD = round((ISDD*FEdd)/1000, 1)
E_trans_ISDI1 = round(FE_trans * dist_chantier_exutoire * (ISDI1 + mav5e * (cam5/100) * pass_ISDI1 + mav4e * (cam4/100) * pass_ISDI1), 1)
E_trans_ISDI2 = round(FE_trans * dist_chantier_exutoire * (ISDI2 + mav5e * (cam5/100) * pass_ISDI2 + mav4e * (cam4/100) * pass_ISDI2), 1)
E_trans_ISDND = round(FE_trans * dist_chantier_exutoire * (ISDND + mav5e * (cam5/100) * pass_ISDND + mav4e * (cam4/100) * pass_ISDND), 1)
E_trans_ISDD = round(FE_trans * dist_chantier_exutoire * (ISDD + mav5e * (cam5/100) * pass_ISDD + mav4e * (cam4/100) * pass_ISDD), 1)

with st.expander("Emissions de CO2e par types de déchets :"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Terres")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(E_ISDI1)
        st.write("CO2e transport (en tCO2e):")
        st.subheader(E_trans_ISDI1)
        st.write("CO2e total (en tCO2e):")
        st.subheader(E_ISDI1+E_trans_ISDI1)
        if ISDI1 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(round(((E_ISDI1 + E_trans_ISDI1)/ISDI1)*1000, 1))
    with col2:
        st.subheader("Gravats")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(E_ISDI2)
        st.write("CO2e transport (en tCO2e):")
        st.subheader(E_trans_ISDI2)
        st.write("CO2e total (en tCO2e):")
        st.subheader(E_ISDI2 + E_trans_ISDI2)
        if ISDI2 > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(round(((E_ISDI2 + E_trans_ISDI2)/ISDI2)*1000, 1))
    with col3:
        st.subheader("DND")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(E_ISDND)
        st.write("CO2e transport (en tCO2e):")
        st.subheader(E_trans_ISDND)
        st.write("CO2e total (en tCO2e):")
        st.subheader(E_ISDND + E_trans_ISDND)
        if ISDND > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(round(((E_ISDND + E_trans_ISDND)/ISDND)*1000, 1))
    with col4:
        st.subheader("DD")
        st.write("CO2e valorisation (en tCO2e):")
        st.subheader(E_ISDD)
        st.write("CO2e transport (en tCO2e):")
        st.subheader(E_trans_ISDD)
        st.write("CO2e total (en tCO2e):")
        st.subheader(E_ISDD + E_trans_ISDD)
        if ISDD > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(round(((E_ISDD + E_trans_ISDD)/ISDD)*1000, 1))


with st.expander("Emissions totales de CO2e (en tCO2e):"):
    E_trans = round(FE_trans * dist_chantier_exutoire * (tot_D + mav5e * (cam5 / 100) * pass_tot + mav4e * (cam4 / 100) * pass_tot), 1)
    E_valo = round(E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD, 1)
    E_tot = E_trans + E_valo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Transport :")
        st.subheader(E_trans)
    with col2:
        st.write("Valorisation :")
        st.subheader(E_valo)
    with col3:
        st.write("Total des émissions :")
        st.subheader(round(E_tot, 1))
    with col4:
        if tot_D > 0:
            st.write("kgCO2e/tonne :")
            st.subheader(round(((E_trans+E_valo)/tot_D)*1000), 1)

st.header("Réduire l'empreinte carbone")

#Réutiliser 10% des terres sur site
action1 = st.checkbox('Augmenter de 10% la réutilisation des terres sur site')
if action1:
    if valo_terres >= 10:
        new_valo_terres = valo_terres - 10
        new_ISDI1 = ISDI1brut * (new_valo_terres/100)
        new_E_ISDI1 = (new_ISDI1 * FEterres)/1000
        new_pass_ISDI1 = math.ceil(new_ISDI1/(load_cam5*(cam5/100)+load_cam4*(cam4/100)))
        new_E_trans_ISDI1 = FE_trans * dist_chantier_exutoire * (new_ISDI1 + mav5e * (cam5 / 100) * new_pass_ISDI1 + mav4e * (cam4 / 100) * new_pass_ISDI1)
        Ea1 = E_ISDI1+E_trans_ISDI1-new_E_ISDI1-new_E_trans_ISDI1
        st.write("Cette action permet de réduire les émissions totales de :")
        st.subheader(str(round(Ea1, 1)) + " tCO2e")
        v = random.choice([str(math.ceil(Ea1 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea1 * 5181)) + " km en voiture (" + str(math.ceil(Ea1 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea1)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea1 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea1 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea1 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea1 * 43)) + " jeans en coton 👖"])
        st.subheader("Soit " + v)
    else:
        st.error("Le taux de réutilisation des terres sur site est déjà supérieur à 85%")

#Privilégier les camions 5 essieux (de 70% à 80%)
action2 = st.checkbox("Utiliser 15% de camions 5 essieux en plus")
if action2:
    if cam5 <= 85:
        new_cam5 = cam5 + 15
        new_cam4 = 100 - new_cam5
        new_FE_trans = FEmoy5e * (new_cam5 / 100) + FEmoy4e * (new_cam4 / 100)
        new_E_trans_ISDI1 = round(new_FE_trans * dist_chantier_exutoire * (ISDI1 + mav5e * (new_cam5 / 100) * pass_ISDI1 + mav4e * (new_cam4 / 100) * pass_ISDI1), 1)
        new_E_trans_ISDI2 = round(new_FE_trans * dist_chantier_exutoire * (ISDI2 + mav5e * (new_cam5 / 100) * pass_ISDI2 + mav4e * (new_cam4 / 100) * pass_ISDI2), 1)
        new_E_trans_ISDND = round(new_FE_trans * dist_chantier_exutoire * (ISDND + mav5e * (new_cam5 / 100) * pass_ISDND + mav4e * (new_cam4 / 100) * pass_ISDND), 1)
        new_E_trans_ISDD = round(new_FE_trans * dist_chantier_exutoire * (ISDD + mav5e * (new_cam5 / 100) * pass_ISDD + mav4e * (new_cam4 / 100) * pass_ISDD), 1)
        new_pass_ISDI1 = math.ceil(ISDI1 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
        new_pass_ISDI2 = math.ceil(ISDI2 / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
        new_pass_ISDND = math.ceil(ISDND / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
        new_pass_ISDD = math.ceil(ISDD / (load_cam5 * (new_cam5 / 100) + load_cam4 * (new_cam4 / 100)))
        new_pass_tot = new_pass_ISDI1+new_pass_ISDI2+new_pass_ISDND+new_pass_ISDD
        new_E_trans = new_FE_trans * dist_chantier_exutoire * (tot_D + mav5e * (new_cam5 / 100) * new_pass_tot + mav4e * (new_cam4 / 100) * new_pass_tot)
        st.write("Cette action permet de réduire les émissions totales de :")
        Ea2 = round(E_trans - new_E_trans, 1)
        st.subheader(str(Ea2) + " tCO2e")
        w = random.choice([str(math.ceil(Ea2*138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea2*5181)) + " km en voiture (" + str(math.ceil(Ea2 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea2)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea2*54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea2*61)) + " smartphones 📱",
                           str(math.ceil(Ea2*2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea2*43)) + " jeans en coton 👖"])
        st.subheader("Soit " + w)
    else:
        st.error("Le taux d'utilisation de 5 essieux est déjà supérieur à 90%")

#Optimiser le chargement de 2 tonnes (borner l'action)
action3 = st.checkbox('Optimiser le chargement moyen des camions de 2 tonnes')
if action3:
    new_load_cam5 = load_cam5 + 2
    new_load_cam4 = load_cam4 + 2
    new_pass_ISDI1 = math.ceil(ISDI1 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
    new_pass_ISDI2 = math.ceil(ISDI2 / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
    new_pass_ISDND = math.ceil(ISDND / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
    new_pass_ISDD = math.ceil(ISDD / (new_load_cam5 * (cam5 / 100) + new_load_cam4 * (cam4 / 100)))
    new_pass_tot = new_pass_ISDI1 + new_pass_ISDI2 + new_pass_ISDND + new_pass_ISDD
    new_E_trans = round(FE_trans * dist_chantier_exutoire * (tot_D + mav5e * (cam5 / 100) * new_pass_tot + mav4e * (cam4 / 100) * new_pass_tot), 1)
    st.write("Cette action permet de réduire les émissions totales de :")
    Ea3 = E_trans - new_E_trans
    st.subheader(str(round(Ea3, 1)) + " tCO2e")
    x = random.choice([str(math.ceil(Ea3 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea3 * 5181)) + " km en voiture (" + str(math.ceil(Ea3 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea3)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea3 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea3 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea3 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea3 * 43)) + " jeans en coton 👖"])
    st.subheader("Soit " + x)

#Choix d'un exutoire 10 km plus proche
action4 = st.checkbox("Choisir un exutoire 10 km plus proche")
if action4:
    if dist_chantier_exutoire >= 10:
        new_dist_chantier_exutoire = dist_chantier_exutoire - 10
        new_E_trans = round(FE_trans * new_dist_chantier_exutoire * (tot_D + mav5e * (cam5 / 100) * pass_tot + mav4e * (cam4 / 100) * pass_tot), 1)
        st.write("Cette action permet de réduire les émissions totales de :")
        Ea4 = E_trans - new_E_trans
        st.subheader(str(round(Ea4, 1)) + " tCO2e")
        y = random.choice([str(math.ceil(Ea4 * 138)) + " repas avec du boeuf 🥩",
                           str(math.ceil(Ea4 * 5181)) + " km en voiture (" + str(math.ceil(Ea4 * 8)) + " trajets Paris-Marseille) 🚗",
                           str(math.ceil(Ea4)) + " aller-retour Paris-NYC ✈️",
                           str(math.ceil(Ea4 * 54)) + " jours de chauffage (gaz) 🌡️",
                           str(math.ceil(Ea4 * 61)) + " smartphones 📱",
                           str(math.ceil(Ea4 * 2208)) + " litres d'eau en bouteille 🧴",
                           str(math.ceil(Ea4 * 43)) + " jeans en coton 👖"])
        st.subheader("Soit " + y)
    else:
        st.error("L'exutoire se trouve déjà à moins de 10 km du chantier")

#Résultats total + équivalences CO2e
action5 = st.checkbox("Combiner toutes les actions de réduction")
if action5:
    new_dist_chantier_exutoire = dist_chantier_exutoire - 10
    new_valo_terres = valo_terres - 10
    new_cam5 = cam5 + 15
    new_cam4 = 100 - new_cam5
    new_FE_trans = FEmoy5e * (new_cam5 / 100) + FEmoy4e * (new_cam4 / 100)
    new_load_cam5 = load_cam5 + 2
    new_load_cam4 = load_cam4 + 2
    new_ISDI1 = ISDI1brut * (new_valo_terres / 100)

    new_E_ISDI1 = (new_ISDI1 * FEterres) / 1000
    new_pass_ISDI1 = math.ceil(new_ISDI1 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
    new_pass_ISDI2 = math.ceil(ISDI2 / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
    new_pass_ISDND = math.ceil(ISDND / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
    new_pass_ISDD = math.ceil(ISDD / (new_load_cam5 * (new_cam5 / 100) + new_load_cam4 * (new_cam4 / 100)))
    new_tot_D = new_ISDI1 + ISDI2 + ISDND + ISDD
    new_pass_tot = new_pass_ISDI1 + new_pass_ISDI2 + new_pass_ISDND + new_pass_ISDD
    new_E_trans = round(new_FE_trans * new_dist_chantier_exutoire * (new_tot_D + mav5e * (new_cam5 / 100) * new_pass_tot + mav4e * (new_cam4 / 100) * new_pass_tot), 1)
    new_E_valo = round(new_E_ISDI1 + E_ISDI2 + E_ISDND + E_ISDD, 1)
    new_E_tot = new_E_trans + new_E_valo
    st.write("L'ensemble des actions combinées permet de réduire les émissions totales de :")
    Ea5 = E_tot - new_E_tot
    st.subheader(str(round(Ea5, 1)) + " tCO2e")
    z = random.choice([str(math.ceil(Ea5 * 138)) + " repas avec du boeuf 🥩",
                       str(math.ceil(Ea5 * 5181)) + " km en voiture (" + str(math.ceil(Ea5 * 8)) + " trajets Paris-Marseille) 🚗",
                       str(math.ceil(Ea5)) + " aller-retour Paris-NYC ✈️",
                       str(math.ceil(Ea5 * 54)) + " jours de chauffage (gaz) 🌡️",
                       str(math.ceil(Ea5 * 61)) + " smartphones 📱",
                       str(math.ceil(Ea5 * 2208)) + " litres d'eau en bouteille 🧴",
                       str(math.ceil(Ea5 * 43)) + " jeans en coton 👖"])
    st.subheader("Soit " + z)
    conso_moy = 30 / 100
    conso_tot = conso_moy * pass_tot
    new_conso_tot = conso_moy * new_pass_tot
    prix_c = 2
    eco = (conso_tot-new_conso_tot)*prix_c
    st.write(str(eco))

st.header("Estimation des gains €")



st.write("")
st.write("")
st.caption("""Les données sources utilisées sont référencées et disponible sur demande à Altaroad

Développé par Altaroad - CONFIDENTIEL 2022 - https://www.altaroad.com""")