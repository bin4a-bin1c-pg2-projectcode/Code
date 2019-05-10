from Bio.Blast import NCBIWWW
import pandas
import time
import datetime


def main():
    bestand_lijstsequenties, bestand_lijstsheaders = bestandinlezen()
    blast(bestand_lijstsequenties, bestand_lijstsheaders)
    gegevens_blast(bestand_lijstsheaders, bestand_lijstsequenties)


def bestandinlezen():
    bestand = pandas.read_excel("Course4_dataset_v03.xlsx", header=None, sheet_name="groep11")

    bestand_lijstsequenties = []
    bestand_lijstsheaders = []
    for i in range(100):
        x = i
        test = bestand.iloc[x, 1]
        test1 = bestand.iloc[x, 4]
        test_ = bestand.iloc[x, 0]
        test_2 = bestand.iloc[x, 3]
        bestand_lijstsequenties.append(test)
        bestand_lijstsequenties.append(test1)
        bestand_lijstsheaders.append(test_)
        bestand_lijstsheaders.append(test_2)

    return bestand_lijstsequenties, bestand_lijstsheaders


def blast(bestand_lijstsequenties, bestand_lijstheaders):
    bestand = open("test.xml", "w")
    for i in range(4):
        time.sleep(15)
        print("De blast gaat beginnen ", "Nummer: ", i, "Op datum: ", datetime.datetime.now())
        result_handle = NCBIWWW.qblast(program="tblastx", database="nr", sequence=bestand_lijstsequenties[i],
                                       matrix_name="BLOSUM62", expect=4, alignments=1, hitlist_size=10)
        print("De blast is gestopt ", "Nummer:", i, "Op datum: ", datetime.datetime.now())
        bestand.write(bestand_lijstheaders[i] + "\n")
        bestand.write(result_handle.getvalue())


def gegevens_blast(bestand_lijstsheaders, bestand_lijstsequenties):
    bestand = open("test.xml")
    bestand_resultaten = open("resultaten.txt", "w")
    hit = False
    count = -1
    for regel in bestand:
        regel = regel.replace("\n", "")
        if regel.startswith("@"):
            count += 1
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
                bestand_resultaten.write("*** Nieuw resultaat ***" + "\n")
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("Beschrijving: " + split[1] + "\n")
            if "<Hit_accession" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("Accessie code: " + split[1] + "\n")
            if "<Hsp_score>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("Score: " + split[1] + "\n")
            if "<Hsp_evalue>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                bestand_resultaten.write("E-value: " + split[1] + "\n")
            if "<Hsp_query-from>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                query_from = int(split[1])
            if "<Hsp_query-to>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                query_to = int(split[1])
                query_cover = ((int(query_to) - int(query_from)) / int(query_len)) * 100
                bestand_resultaten.write("Query cover: " + str(query_cover) + "%" + "\n")
            if "<Hsp_identity>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                hsp_identity = int(split[1])
            if "<Hsp_align-len>" in regel:
                regel = regel.split("<")
                split = regel[1].split(">")
                hsp_align_len = int(split[1])
                identity = (int(hsp_identity) / int(hsp_align_len)) * 100
                bestand_resultaten.write("Percentage Identity: " + str(identity) + "%" + "\n" + "\n")
                hit = False


main()

