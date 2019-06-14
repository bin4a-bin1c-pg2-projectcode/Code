from Bio.Blast import NCBIWWW
import pandas
import time
import datetime


def main():
    bestand_lijstsequenties, bestand_lijstsheaders = bestandinlezen()  # hiermee wordt het bestand ingelezen
    blast(bestand_lijstsequenties, bestand_lijstsheaders)  # Deze functie voert het blasten uit
    gegevens_blast(bestand_lijstsheaders, bestand_lijstsequenties)  # Deze functie maakt het tekstbestand aan voor de
    # database


def bestandinlezen():
    """ Deze functie gaat een excel bestand openen met panda, groep11 van het excel bestand. Dan worden er 2 lijsten
    aangemaakt, een voor de haders, een voor de sequenties. Dan voor elke regel in het bestand voor range 100 worden
    allebei de headers en allebei de sequenties in de lijsten toegevoegd. Deze lijsten worden gereturnd

    :return header en sequentie lijst
    """
    bestand = pandas.read_excel("Course4_dataset_v03.xlsx", header=None, sheet_name="groep11")

    bestand_lijstsequenties = []
    bestand_lijstsheaders = []
    for i in range(100):
        x = i
        read1 = bestand.iloc[x, 1]  # in deze regel staat de eeste sequentie
        read2 = bestand.iloc[x, 4]  # in deze regel staat de tweede sequentie
        header_read1 = bestand.iloc[x, 0]  # in deze regel staat de eerste header
        header_read2 = bestand.iloc[x, 3]  # in deze regel staat de tweede header
        bestand_lijstsequenties.append(read1)
        bestand_lijstsequenties.append(read2)
        bestand_lijstsheaders.append(header_read1)
        bestand_lijstsheaders.append(header_read2)

    return bestand_lijstsequenties, bestand_lijstsheaders


def blast(bestand_lijstsequenties, bestand_lijstheaders):
    """ Deze functie opent een xml file die leeg is. Daarna voor de lengte van de sequentielijst wordt eerst een 15
    sec pauze in het script. Het scirpt laat zien waar hij in de lijst zit, daarna gaat het script met biopython de
    blast uitvoeren voor de index van de range in de sequentielijst met de aangegeven parameters. De resultaten worden
    in het xml file geschreven.

    :param bestand_lijstsequenties, een lijst met alle sequenties
    :param bestand_lijstheaders, een lijst met alle headers
    :return xml file die na elke blast wordt aangepast en op het laatst wordt weggeschreven
    """
    bestand = open("blastx.xml", "w")
    for i in range(len(bestand_lijstsequenties)):
        time.sleep(15)
        # deze print helpt mee dat je kan zien of het script nog bezig is, en waar het is
        print("De blast gaat beginnen ", "Nummer: ", i, "Op datum: ", datetime.datetime.now())
        result_handle = NCBIWWW.qblast(program="blastx", database="nr", sequence=bestand_lijstsequenties[i],
                                       matrix_name="BLOSUM62", expect=4, alignments=1, hitlist_size=10)
        print("De blast is gestopt ", "Nummer:", i, "Op datum: ", datetime.datetime.now())
        bestand.write(bestand_lijstheaders[i] + "\n")
        bestand.write(result_handle.getvalue())


def gegevens_blast(bestand_lijstsheaders, bestand_lijstsequenties):
    """ Deze functie opent het bestand met de blastresultaten en opent een nieuw tekstbestand. Voor elke regel in het
    bestand worden eerst de enters weggehaald. Daarna als de regel start met @, wordt de header en sequentie van de
    bijbehorende index in het bestand geschreven. Als de regel met Hit begint, wordt hit op True gezet en wordt
    de query_lengte, beschrijving, accessiecode, score, E-value en wordt de query cover en de percentage identity
    berekent. Dit allemaal wordt in het bestand weggeschreven.

    :param bestand_lijstsequenties, een lijst met de sequenties
    :param bestand_lijstsheaders, een lijst met de headers
    :return bestand
    """
    bestand = open("blastx.xml")
    bestand_resultaten = open("resultaten_blastx.txt", "w")
    hit = False
    count = -1
    for regel in bestand:
        regel = regel.replace("\n", "")
        if regel.startswith("@"):
            count += 1
            # zo krijg je in het bestand de header en sequentie te zien waar de resultaten bij horen
            bestand_resultaten.write(bestand_lijstsheaders[count] + "\n")
            bestand_resultaten.write(bestand_lijstsequenties[count] + "\n")
        if regel == "<Hit>":
            hit = True
        if "<BlastOutput_query-len>" in regel:
            regel = regel.split("<")
            split = regel[1].split(">")
            query_len = int(split[1])
        if hit is True:
            if "<Hit_def" in regel:
                # dit geeft aan waar een nieuw resultaat begint
                bestand_resultaten.write("*** Nieuw resultaat ***" + "\n")
                regel = regel.split("<")
                split = regel[1].split(">")
                # deze geeft de naam van het organisme mee met eventueel een eiwitnaam
                bestand_resultaten.write("Beschrijving: " + split[1] + "\n")
            if "<Hit_accession" in regel:
                # dit geeft aan wat de accessiecode is
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("Accessie code: " + split[1] + "\n")
            if "<Hsp_score>" in regel:
                # dit geeft de score mee van het resultaat
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("Score: " + split[1] + "\n")
            if "<Hsp_evalue>" in regel:
                # dit geeft de e-value mee
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("E-value: " + split[1] + "\n")
            if "<Hsp_query-from>" in regel:
                # dit geeft de query from mee om de query cover te bepalen
                regel = regel.split("<")
                split = regel[1].split(">")
                query_from = int(split[1])
            if "<Hsp_query-to>" in regel:
                # dit haalt de query to op en gaat daarna de query cover berekenen
                regel = regel.split("<")
                split = regel[1].split(">")
                query_to = int(split[1])
                query_cover = ((int(query_to) - int(query_from)) / int(query_len)) * 100
                bestand_resultaten.write("Query cover: " + str(query_cover) + "%" + "\n")
            if "<Hsp_identity>" in regel:
                # deze geeft de aantal identitys mee
                regel = regel.split("<")
                split = regel[1].split(">")
                hsp_identity = int(split[1])
            if "<Hsp_align-len>" in regel:
                # deze gaat het identity percentage berekenen
                regel = regel.split("<")
                split = regel[1].split(">")
                hsp_align_len = int(split[1])
                identity = (int(hsp_identity) / int(hsp_align_len)) * 100
                bestand_resultaten.write("Percentage Identity: " + str(identity) + "%" + "\n" + "\n")
                hit = False
    print("Het script is afgelopen")


main()
