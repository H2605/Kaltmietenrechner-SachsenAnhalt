import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
# URL der Webseite
st.title("Kaltmieten Rechner Sachsen Anhalt(Wohnungen)")

places_list=["Aken-Elbe","Aland","Allstedt","Alsleben-Saale","Altenhausen","Altmaerkische-Hoehe",
             "Altmaerkische-Wische","Am-Großen-Bruch","An-der-Poststraße","Angern","Annaburg","Apenburg-Winterfeld",
             "Arendsee-Altmark","Arneburg","Arnstein","Aschersleben","Ausleben","Bad-Bibra","Bad-Duerrenberg",
             "Bad-Lauchstaedt","Bad-Schmiedeberg","Balgstaedt","Ballenstedt","Barby","Barleben","Barnstaedt","Beendorf",
             "Beetzendorf","Benndorf","Berga-Kyffhaeuser","Bernburg-Saale","Biederitz","Bismark-Altmark","Bitterfeld-Wolfen",
             "Blankenburg-Harz","Blankenheim","Boerdeaue","Boerde-Hakel","Boerdeland","Borne","Bornstedt","Braunsbedra",
             "Bruecken-Hackpfueffel","Buelstringen","Burg","Burgstall","Calbe-Saale","Calvoerde","Colbitz","Coswig-Anhalt",
             "Daehre","Dessau-Roßlau","Diesdorf","Ditfurt","Droyßig","Eckartsberga","Edersleben","Egeln","Eichstedt-Altmark",
             "Eilsleben","Lutherstadt-Eisleben","Lutherstadt-Wittenberg","Elsteraue","Erxleben","Falkenstein-Harz",
             "Farnstaedt","Finne","Finneland","Flechtingen","Freyburg-Unstrut","Gardelegen","Genthin","Gerbstedt",
             "Giersleben","Gleina","Goldbeck","Gommern","Goseck","Graefenhainichen","Groeningen","Groß-Quenstedt","Guesten",
             "Gutenborn","Halberstadt","Haldensleben","Halle-Saale","Harbke","Harsleben","Harzgerode","Hassel","Havelberg",
             "Hecklingen","Hedersleben","Helbra","Hergisdorf","Hettstedt","Hohe-Boerde","Hohenberg-Krusemark","Hohenmoelsen",
             "Hoetensleben","Huy","Iden","Ilberstedt","Ilsenburg-Harz","Ingersleben","Jerichow","Jessen-Elster","Juebar",
             "Kabelsketal","Kaiserpfalz","Kalbe-Milde","Kamern","Karsdorf","Kelbra-Kyffhaeuser","Kemberg","Klietz",
             "Klostermansfeld","Kloetze","Koennern","Koethen-Anhalt","Kretzschau","Kroppenstedt","Kuhfelde","Landsberg",
             "Lanitz-Hassel-Tal","Laucha-an-der-Unstrut","Leuna","Loitsche-Heinrichsberg","Luetzen","Magdeburg","Mansfeld",
             "Meineweh","Merseburg","Mertendorf","Moeckern","Molauer-Land","Moeser","Muecheln-Geiseltal","Muldestausee",
             "Naumburg-Saale","Nebra-Unstrut","Nemsdorf-Goehrendorf","Niedere-Boerde","Nienburg-Saale","Nordharz",
             "Oberharz-am-Brocken","Obhausen","Oebisfelde-Weferlingen","Oranienbaum-Woerlitz","Oschersleben-Bode",
             "Osterburg-Altmark","Osterfeld","Osternienburger-Land","Osterwieck","Petersberg","Ploetzkau","Quedlinburg",
             "Querfurt","Raguhn-Jeßnitz","Rochau","Rogaetz","Rohrberg","Salzatal","Salzwedel","Sandau-Elbe",
             "Sandersdorf-Brehna","Sangerhausen","Schkopau","Schnaudertal","Schollene","Schoenburg","Schoenebeck-Elbe",
             "Schoenhausen-Elbe","Schraplau","Schwanebeck","Seegebiet-Mansfelder-Land","Seehausen-Altmark","Seeland",
             "Selke-Aue","Sommersdorf","Staßfurt","Steigra","Stendal","Stoeßen","Suedharz","Suedliches-Anhalt","Suelzetal",
             "Tangerhuette","Tangermuende","Teuchern","Teutschenthal","Thale","Ummendorf","Voelpke","Wallhausen","Wallstawe",
             "Wanzleben-Boerde","Wefensleben","Wegeleben","Weißenfels","Werben-Elbe","Wernigerode","Westheide","Wethau",
             "Wetterzeube","Wettin-Loebejuen","Wimmelburg","Wittenberg,-Lutherstadt","Wolmirsleben","Wolmirstedt",
             "Wust-Fischbeck","Zahna-Elster","Zehrental","Zeitz","Zerbst-Anhalt","Zielitz","Zoerbig"]
place=st.selectbox(label="Gemeinde in Sachsen Anhalt auswählen",options=places_list)
placelow=str.lower(place)
try:
    url = "https://www.engelvoelkers.com/de-de/mietspiegel/sachsen-anhalt/"+placelow+"/"



    # Sende eine GET-Anfrage an die Webseite
    response = requests.get(url)
    st.text(response)
    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Den HTML-Inhalt der Seite parsen
        soup = BeautifulSoup(response.content, 'html.parser')
        st.text("Verbindung erfolgreich")

    else:
        st.text(print(f"Fehler beim Abrufen der Seite: {response.status_code}"))

    body=soup.body.div
    stringer=body.contents[13]("p")
    stranger=str(stringer)
    stranger
    pattern = r"(\d+,\d{2})"

    # Suche nach dem Muster
    match = re.search(pattern, stranger)
    preis=match.group(1)

    people=st.slider(label="Anzahl der Personen",value=1, min_value=1 )
    size=st.slider(label="Wohnfläche in qm", max_value=1000, min_value=5,value=20)
    zustand=st.slider(label="Zustand der Wohnung", min_value=0, max_value=10, step=1, value=5)
    yearbuild=st.number_input(label="Jahr der Errichtung", min_value=1800, max_value= datetime.now().year, value=1950)
    yearres=st.number_input(label="Jahr der letzten Sanierung", min_value=1800, max_value= datetime.now().year,value=1950)

    st.text("Der Preis pro Quadratmeter in "+place+" beträgt "+preis+"€ .")
    preis=preis.replace(",",".")
    #st.text(type(preis))
    preis=float(preis)

    gewichtung_baujahr = 0.02  # 2% Veränderung pro Dekade
    gewichtung_sanierung = 0.04  # 3% pro Dekade seit der letzten Sanierung
    gewichtung_zustand = 0.04  # 5% je nach Zustand der Wohnung

    baujahr_abweichung = (datetime.now().year - yearbuild) / 10 * -gewichtung_baujahr
    sanierung_abweichung = (datetime.now().year - yearres) / 10 * -gewichtung_sanierung

    zustand_abweichung = (zustand - 3) * gewichtung_zustand  # 3 ist der Durchschnittszustand
    gesamt_abweichung = 1 + baujahr_abweichung + sanierung_abweichung + zustand_abweichung

    mietpreis_pro_qm = preis * gesamt_abweichung
    mietpreis_gesamt = mietpreis_pro_qm * size
    mietpreis_gesamt=round(mietpreis_gesamt, 2)
    #mietpreis_gesamt=mietpreis_gesamt.replace(",",".")
    mietpreis_gesamt=str(mietpreis_gesamt)

    st.text("Die Miete für die Wohnung sollte "+mietpreis_gesamt+"€ betragen.")
except:
  print("Für den ausgewählen Ort gibt es leider keinen Mietspiegel")