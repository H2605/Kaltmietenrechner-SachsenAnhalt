import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import numpy as np

st.title("Kaltmieten Rechner Sachsen Anhalt(Wohnungen)")
bl_list=["Baden-Württemberg","Bayern","Berlin","Brandenburg","Bremen","Hamburg","Hessen","Mecklenburg-Vorpommern",
         "Niedersachsen","Nordrhein-Westfalen","Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt","Schleswig-Holstein","Thüringen"]
bl=st.selectbox(label="Bundesland auswählen", options=bl_list)
bl_low=str.lower(bl)
places_nrw=["Aachen","Ahaus","Ahlen","Aldenhoven","Alfter","Alpen-Niederrhein","Alsdorf","Altena","Altenbeken","Altenberge","Anroechte",
            "Arnsberg","Ascheberg-Westfalen","Attendorn","Augustdorf","Bad-Berleburg","Bad-Driburg","Bad-Honnef","Bad-Laasphe","Bad-Lippspringe",
            "Bad-Muenstereifel","Bad-Oeynhausen","Bad-Salzuflen","Bad-Sassendorf","Bad-Wuennenberg","Baesweiler","Balve","Barntrup","Beckum",
            "Bedburg","Bedburg-Hau","Beelen","Bergheim","Bergisch-Gladbach","Bergkamen","Bergneustadt","Bestwig","Beverungen","Bielefeld",
            "Billerbeck","Blankenheim-Ahr","Blomberg","Bocholt","Bochum","Boenen","Bonn","Borchen","Borgentreich","Borgholzhausen","Borken",
            "Bornheim-Rheinland","Bottrop","Brakel","Breckerfeld","Brilon","Brueggen","Bruehl-Rheinland","Buende","Burbach-Siegerland",
            "Bueren-Westfalen","Burscheid","Castrop-Rauxel","Coesfeld","Dahlem-Nordeifel","Datteln","Delbrueck","Detmold","Dinslaken",
            "Doerentrup","Dormagen","Dorsten","Dortmund","Drensteinfurt","Drolshagen","Duisburg","Duelmen","Dueren","Duesseldorf","Eitorf",
            "Elsdorf-Rheinland","Emmerich-am-Rhein","Emsdetten","Engelskirchen","Enger","Ennepetal","Ennigerloh","Ense","Erftstadt","Erkelenz",
            "Erkrath","Erndtebrueck","Erwitte","Eschweiler","Eslohe-Sauerland","Espelkamp","Essen","Euskirchen","Everswinkel","Extertal",
            "Finnentrop","Frechen","Freudenberg-Siegerland","Froendenberg-Ruhr","Gangelt","Geilenkirchen","Geldern","Gelsenkirchen","Gescher",
            "Geseke","Gevelsberg","Gladbeck","Goch","Grefrath","Greven","Grevenbroich","Gronau-Westf.","Gummersbach","Guetersloh","Haan","Hagen",
            "Hallenberg","Halle-Westf.","Haltern-am-See","Halver","Hamm","Hamminkeln","Harsewinkel","Hattingen","Havixbeck","Heek",
            "Heiden-Muensterland","Heiligenhaus","Heimbach-Eifel","Heinsberg","Hellenthal","Hemer","Hennef-Sieg","Herdecke","Herford","Herne",
            "Herscheid","Herten","Herzebrock-Clarholz","Herzogenrath","Hiddenhausen","Hilchenbach","Hilden","Hille","Holzwickede","Hopsten",
            "Horn-Bad-Meinberg","Hoerstel","Horstmar","Hoevelhof","Hoexter","Hueckelhoven","Hueckeswagen","Huellhorst","Huenxe","Huertgenwald",
            "Huerth","Ibbenbueren","Inden-Rheinland","Iserlohn","Isselburg","Issum","Juechen","Juelich","Kaarst","Kalkar","Kall","Kalletal",
            "Kamen","Kamp-Lintfort","Kempen","Kerken","Kerpen","Kevelaer","Kierspe","Kirchhundem","Kirchlengern","Kleve","Koeln","Koenigswinter",
            "Korschenbroich","Kranenburg-Niederrhein","Krefeld","Kreuzau","Kreuztal","Kuerten","Ladbergen","Laer","Lage-Lippe","Langenberg-Guetersloh",
            "Langenfeld-Rheinland","Langerwehe","Legden","Leichlingen-Rheinland","Lemgo","Lengerich-Westfalen","Lennestadt","Leopoldshoehe","Leverkusen",
            "Lichtenau-Westfalen","Lienen","Lindlar","Linnich","Lippetal","Lippstadt","Lohmar","Loehne","Lotte-Westfalen","Luebbecke","Luedenscheid",
            "Luedinghausen","Luegde","Luenen","Marienheide","Marienmuenster","Marl","Marsberg","Mechernich","Meckenheim-Rheinland","Medebach","Meerbusch",
            "Meinerzhagen","Menden-Sauerland","Merzenich","Meschede","Metelen","Mettingen","Mettmann","Minden","Moers","Moehnesee-Gemeinde",
            "Moenchengladbach","Monheim-am-Rhein","Monschau","Morsbach","Much","Muelheim-an-der-Ruhr","Muenster-Westfalen","Nachrodt-Wiblingwerde",
            "Netphen","Nettersheim","Nettetal","Neuenkirchen-Steinfurt","Neuenrade","Neukirchen-Vluyn","Neunkirchen-Siegerland","Neunkirchen-Seelscheid",
            "Neuss","Nideggen","Niederkassel","Niederkruechten","Niederzier","Nieheim","Nordkirchen","Nordwalde","Noervenich","Nottuln","Nuembrecht",
            "Oberhausen","Ochtrup","Odenthal","Oelde","Oer-Erkenschwick","Oerlinghausen","Olfen","Olpe","Olsberg","Ostbevern","Overath","Paderborn",
            "Petershagen","Plettenberg","Porta-Westfalica-Stadt","Preußisch-Oldendorf","Pulheim","Radevormwald","Raesfeld","Rahden","Ratingen",
            "Recke-Westfalen","Recklinghausen","Rees","Reichshof","Reken","Remscheid","Rheda-Wiedenbrueck","Rhede","Rheinbach","Rheinberg","Rheine",
            "Rheurdt","Rietberg","Roedinghausen","Roetgen","Rommerskirchen","Rosendahl","Roesrath","Ruppichteroth","Ruethen","Saerbeck","Salzkotten",
            "Sankt-Augustin","Sassenberg","Schalksmuehle","Schermbeck","Schieder-Schwalenberg","Schlangen-Gemeinde","Schleiden","Schloß-Holte-Stukenbrock",
            "Schmallenberg","Schoeppingen","Schwalmtal-Niederrhein","Schwelm","Schwerte","Selfkant","Selm","Senden-Westfalen","Sendenhorst","Siegburg",
            "Siegen","Simmerath","Soest","Solingen","Sonsbeck","Spenge","Sprockhoevel","Stadtlohn","Steinfurt","Steinhagen-Westfalen",
            "Steinheim-Westfalen","Stemwede","Stolberg-Rheinland","Straelen","Suedlohn","Sundern-Sauerland","Swisttal","Tecklenburg","Telgte","Titz",
            "Toenisvorst","Troisdorf","Übach-Palenberg","Uedem","Unna","Velbert","Velen","Verl","Versmold","Vettweiß","Viersen","Vlotho",
            "Voerde-Niederrhein","Vreden","Wachtberg","Wachtendonk","Wadersloh","Waldbroel","Waldfeucht","Waltrop","Warburg","Warendorf","Warstein",
            "Wassenberg","Weeze","Wegberg","Weilerswist","Welver","Wenden-Sauerland","Werdohl","Werl","Wermelskirchen","Werne","Werther-Westf.","Wesel",
            "Wesseling","Westerkappeln","Wetter-Ruhr","Wettringen-Muensterland","Wickede-Ruhr","Wiehl","Willebadessen","Willich","Wilnsdorf","Windeck",
            "Winterberg","Wipperfuerth","Witten","Wuelfrath","Wuppertal","Wuerselen","Xanten","Zuelpich"]
places_sa=["Magdeburg","Ahlsdorf","Aken-Elbe","Aland","Allstedt","Alsleben-Saale","Altenhausen","Altmaerkische-Hoehe",
             "Altmaerkische-Wische","Am-Grossen-Bruch","An-der-Poststrasse","Angern","Annaburg","Apenburg-Winterfeld",
             "Arendsee-Altmark","Arneburg","Arnstein","Aschersleben","Ausleben","Bad-Bibra","Bad-Duerrenberg",
             "Bad-Lauchstaedt","Bad-Schmiedeberg","Balgstaedt","Ballenstedt","Barby","Barleben","Barnstaedt","Beendorf",
             "Beetzendorf","Benndorf","Berga-Kyffhaeuser","Bernburg-Saale","Biederitz","Bismark-Altmark","Bitterfeld-Wolfen",
             "Blankenburg-Harz","Blankenheim","Boerdeaue","Boerde-Hakel","Boerdeland","Borne","Bornstedt","Braunsbedra",
             "Bruecken-Hackpfueffel","Buelstringen","Burg","Burgstall","Calbe-Saale","Calvoerde","Colbitz","Coswig-Anhalt",
             "Daehre","Dessau-Rosslau","Diesdorf","Ditfurt","Droyssig","Eckartsberga","Edersleben","Egeln","Eichstedt-Altmark",
             "Eilsleben","Lutherstadt-Eisleben","Lutherstadt-Wittenberg","Elsteraue","Erxleben","Falkenstein-Harz",
             "Farnstaedt","Finne","Finneland","Flechtingen","Freyburg-Unstrut","Gardelegen","Genthin","Gerbstedt",
             "Giersleben","Gleina","Goldbeck","Gommern","Goseck","Graefenhainichen","Groeningen","Gross-Quenstedt","Guesten",
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
             "Querfurt","Raguhn-Jessnitz","Rochau","Rogaetz","Rohrberg","Salzatal","Salzwedel","Sandau-Elbe",
             "Sandersdorf-Brehna","Sangerhausen","Schkopau","Schnaudertal","Schollene","Schoenburg","Schoenebeck-Elbe",
             "Schoenhausen-Elbe","Schraplau","Schwanebeck","Seegebiet-Mansfelder-Land","Seehausen-Altmark","Seeland",
             "Selke-Aue","Sommersdorf","Stassfurt","Steigra","Stendal","Stoessen","Suedharz","Suedliches-Anhalt","Suelzetal",
             "Tangerhuette","Tangermuende","Teuchern","Teutschenthal","Thale","Ummendorf","Voelpke","Wallhausen","Wallstawe",
             "Wanzleben-Boerde","Wefensleben","Wegeleben","Weissenfels","Werben-Elbe","Wernigerode","Westheide","Wethau",
             "Wetterzeube","Wettin-Loebejuen","Wimmelburg","Wolmirsleben","Wolmirstedt",
             "Wust-Fischbeck","Zahna-Elster","Zehrental","Zeitz","Zerbst-Anhalt","Zielitz","Zoerbig"]
places_list=[]
if bl=="Nordrhein-Westfalen":
   places_list=places_nrw
elif bl=="Sachsen-Anhalt":
   places_list=places_sa

place=st.selectbox(label="Gemeinde im Bundesland auswählen",options=places_list)
placelow=str.lower(place)
try:
    url = "https://www.engelvoelkers.com/de-de/mietspiegel/"+bl_low+"/"+placelow+"/"



    # Sende eine GET-Anfrage an die Webseite
    response = requests.get(url)
    #st.text(response)
    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Den HTML-Inhalt der Seite parsen
        soup = BeautifulSoup(response.content, 'html.parser')
        st.text("Verbindung erfolgreich")

#    else:
#        st.text(print(f"Fehler beim Abrufen der Seite: {response.status_code}"))

    body=soup.body.div
    stringer=body.contents[13]("p")
    stranger=str(stringer)
    #stranger
    pattern = r"(\d+,\d{1,2})€"

    # Suche nach dem Muster
    match = re.search(pattern, stranger)
    preis=match.group(1)

    people=st.slider(label="Anzahl der Personen im Haushalt",value=1, min_value=1, max_value=30 )
    bk_pp=st.number_input(label="Betriebskosten pro Person in €", min_value=0.00, value=30.00)
    size=st.number_input(label="Wohnfläche in m²", max_value=1000, min_value=5,value=20)
    zustand=st.slider(label="Zustand der Wohnung", min_value=0, max_value=10, step=1, value=5, 
                      help='''
                    #   1: Sehr schlechter Zustand: 
                    •    Nicht bewohnbar ohne umfassende Renovierungen
                    #   2: Mangelhafter Zustand 
                    •    Mehrere strukturelle Mängel, die den Wohnkomfort stark beeinträchtigen\n 
                    •    Deutliche Abnutzungserscheinungen, teils beschädigte Böden und Wände, Reparaturen notwendig\n
                    •    Sanierung dringend erforderlich.
                    # 3: Schlechter Zustand
                    •    Spürbare Abnutzung mit alten, nicht mehr zeitgemäßen Elektro- und Sanitärinstallationen\n
                    •    Böden und Wände mit vielen Gebrauchsspuren auf
                    # 4: Unterdurchschnittlicher Zustand
                    •    Leichte bis moderate Abnutzung sichtbar (z.B. Kratzer auf Böden, fleckige Wände).\n
                    •    Funktionsfähige, aber veraltete Installationen und Ausstattung, mit teilweise kleineren Reparaturen erforderlich.\n
                    •    Modernisierung sinnvoll, aber nicht zwingend notwendig
                    # 5: Durchschnittlicher Zustand
                    •    Böden, Wände und sanitäre Anlagen in funktionalem, aber sichtbarem gebrauchten Zustand.\n
                    •    Typische Wohnung, wie sie in älteren Bauten häufig vorkommt.
                    # 6: Überdurchschnittlicher Zustand
                    •    Gute bauliche Substanz ohne erkennbare Schäden, nur leichte Gebrauchsspuren\n
                    •    Kann ohne größere Renovierungen sofort bewohnt werden, aber Modernisierung wäre vorteilhaft
                    # 7: Guter Zustand
                    •   Gut erhalten, gepflegte Wohnung ohne offensichtliche Mängel\n
                    •   Angenehmes Wohnambiente mit nur minimalem Modernisierungsbedarf
                    # 8: Sehr guter Zustand
                    •    Keine sichtbare Abnutzung, Wohnung ist im ausgezeichnetem Zustand\n
                    •    Hoher Wohnkomfort, keine Reparaturen oder Modernisierungen erforderlich
                    # 9: Neuwertiger Zustand
                    •    Wie neu oder kürzlich komplett renoviert\n
                    •    Keine Abnutzung sichtbar, hochwertiger Wohnkomfort
                    # 10: Exzellenter Zustand / Luxusniveau
                    •    Perfekter Zustand, vergleichbar mit einer Neubau- oder Luxuswohnung
''')
    yearbuild=st.number_input(label="Jahr der Errichtung", min_value=1800, max_value= datetime.now().year, value=1950)
    yearres=st.number_input(label="Jahr der letzten Sanierung", min_value=yearbuild, max_value= datetime.now().year,value=yearbuild)
    st.text("Der durchschnittliche Mietspiegel in "+place+" beträgt "+preis+"€ pro m².")
    preis=preis.replace(",",".")
    #st.text(type(preis))
    preis=float(preis)


    gewichtung_baujahr = 0.01  # 2% Veränderung pro Dekade
    gewichtung_sanierung = 0.045  # 3% pro Dekade seit der letzten Sanierung
    gewichtung_zustand = 0.045  # 5% je nach Zustand der Wohnung

    baujahr_abweichung = (datetime.now().year - yearbuild) / 10 * -gewichtung_baujahr
    sanierung_abweichung = (datetime.now().year - yearres) / 10 * -gewichtung_sanierung

    zustand_abweichung = (zustand - 5) * gewichtung_zustand  # 3 ist der Durchschnittszustand
    gesamt_abweichung = 1 + baujahr_abweichung + sanierung_abweichung + zustand_abweichung


    mietpreis_pro_qm = preis * gesamt_abweichung
    mietpreis_gesamt = mietpreis_pro_qm * size
    warmmiete=round(mietpreis_gesamt+(bk_pp*people),2)
    warmmiete=str(warmmiete)
    mietpreis_gesamt=round(mietpreis_gesamt, 2)
    people=str(people)
    #mietpreis_gesamt=mietpreis_gesamt.replace(",",".")
    mietpreis_gesamt=str(mietpreis_gesamt)
    mietpreis_pro_qm=round(mietpreis_pro_qm, 2)
    mietpreis_pro_qm=str(mietpreis_pro_qm)

    st.text("Unter Berücksichtigung der Faktoren Baujahr, Sanierung und Zustand wurde ein Mietpreis von "+mietpreis_pro_qm+"€ pro m² errechnet.\nDie monatliche Kaltmiete für die Wohnung sollte deswegen "+mietpreis_gesamt+"€ betragen.")
    st.text("Mit "+people+" Personen im Haushalt ergibt das eine Warmmiete von "+warmmiete+"€ (Strom und Heizkosten nicht inbegriffen).")
except:
  st.error("Für den ausgewählen Ort ist ein Mietspiegel leider noch nicht verfügbar")