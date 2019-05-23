from flask import Flask, render_template,request
import mysql.connector
from Bio.Seq import Seq, transcribe
import random
import re
from Bio.Alphabet import IUPAC
from Bio.Blast import NCBIWWW, NCBIXML

app = Flask(__name__)


@app.route('/', methods=['get','post'])
def home():
    return render_template('Database_page2.html')


@app.route('/results', methods=['get','post'])
def results():
    verbinding = mysql.connector.connect(host="remotemysql.com",
                                         user="rp5DHKQnCe",
                                         db="rp5DHKQnCe",
                                         passwd="enSHvniY78")
    cursor = verbinding.cursor()
    # lijsten met de waardes van mogelijke filteropties
    lijst = ["checkboxOne", "checkboxTwo", "checkboxThree", "checkboxFour", "checkboxFive", "checkboxSix",
             "checkboxSeven", "checkboxEight", "checkboxNine", "checkboxTen", "checkboxEleven", "checkboxTwelve",
             "checkboxThirteen", "checkboxFourteen", "checkboxFifteen", "checkboxSixteen"]
    lijst_kolommen = ["Blast_type", "Score", "Query_cover", "Percent_ident", "E_value", "Accessiecode", "Organisme",
                      "Taxonomie", "Read_type", "Header", "Sequentie", "Prot_naam", "Prot_locatie", "Bio_domein",
                      "Bio_proces", "Bio_functie"]
    lijst_organisme = ["organisme"]
    lijst_eiwit = ["eiwit"]
    lijst_read = ["checkboxread1", "checkboxread2", "checkboxread3"]
    lijst_blast = ["checkboxblastx", "checkboxtblastx", "checkboxboth"]
    lijst_getallen = ["E-value_value", "Score_value", "Percent identity", "Query cover"]
    lijst_tekens = ["E_value_parameter", "Score_parameter", "percent_identity_parameter", "query_cover_parameter"]
    resultaat_kolommen = []
    resultaat_where = []
    # de filterstappen om de juiste lijsten te krijgen met de waardes  voor de query's
    for item in lijst:
        result = request.form.get(item)
        if result is not None:
            resultaat_kolommen.append(result)
    for item in lijst_organisme:
        result = request.form.get(item)
        if len(result) > 0:
            resultaat_where.append("where Organisme like '%{}%'".format(result))
    for item in lijst_eiwit:
        result = request.form.get(item)
        if len(result) > 0:
            if len(resultaat_where) > 1:
                resultaat_where.append("Prot_naam like '%{}%'".format(result))
            if len(resultaat_where) == 0:
                resultaat_where.append("where Prot_naam like '%{}%'".format(result))
    for item in lijst_read:
        result = request.form.get(item)
        if result is not None:
            if len(resultaat_where) > 0:
                resultaat_where.append("Read_type = {}".format(result))
            if len(resultaat_where) == 0:
                resultaat_where.append("where Read_type = {}".format(result))
    for item in lijst_blast:
        result = request.form.get(item)
        if result is not None:
            if len(resultaat_where) > 0:
                resultaat_where.append("Blast_type = {}".format(result))
            if len(resultaat_where) == 0:
                resultaat_where.append("where Blast_type = {}".format(result))
    e_value = ''
    score = ''
    percentidentity = ''
    querycover = ''
    for item in lijst_getallen:
        index_getal = lijst_getallen.index(item)
        result = request.form.get(item)
        if len(result) > 0:
            if index_getal == 0:
                e_value = result
            if index_getal == 1:
                score = result
            if index_getal == 2:
                percentidentity = result
            if index_getal == 3:
                querycover = result
    for item in lijst_tekens:
        index_getal = lijst_tekens.index(item)
        result = request.form.get(item)
        if len(result) > 0:
            if index_getal == 0 and e_value != '' and len(resultaat_where) > 0:
                resultaat_where.append("E_value {} {}".format(result, e_value))
            elif index_getal == 0 and e_value != '' and len(resultaat_where) == 0:
                resultaat_where.append("where E_value {} {}".format(result, e_value))
            if index_getal == 1 and score != '' and len(resultaat_where) > 0:
                resultaat_where.append("Score {} {}".format(result, score))
            elif index_getal == 1 and score != '' and len(resultaat_where) == 0:
                resultaat_where.append("where Score {} {}".format(result, score))
            if index_getal == 2 and percentidentity != '' and len(resultaat_where) > 0:
                resultaat_where.append("Percent_ident {} {}".format(result, percentidentity))
            elif index_getal == 2 and percentidentity != '' and len(resultaat_where) == 0:
                resultaat_where.append("where Percent_ident {} {}".format(result, percentidentity))
            if index_getal == 3 and querycover != '' and len(resultaat_where) > 0:
                resultaat_where.append("Query_cover {} {}".format(result, percentidentity))
            elif index_getal == 3 and querycover != '' and len(resultaat_where) == 0:
                resultaat_where.append("where Query_cover {} {}".format(result, percentidentity))

    # de query's die worden uitgevoerd
    test = ''
    if len(resultaat_kolommen) == 0:
        query = "select {} from Seq_Blast join Seq_Read SR on Seq_Blast.Blast_ID = SR.Read_ID " \
                "join Eiwitten E on Seq_Blast.Blast_ID = E.Prot_ID".format(" , ".join(lijst_kolommen))
        cursor.execute(query)
        test = cursor.fetchall()
    if len(resultaat_kolommen) == 0 and len(resultaat_where) != 0:
        query = "select {} from Seq_Blast join Seq_Read SR on Seq_Blast.Blast_ID = SR.Read_ID join Eiwitten E on " \
                "Seq_Blast.Blast_ID = E.Prot_ID {}" \
            .format(" , ".join(lijst_kolommen), " and ".join(resultaat_where))
        cursor.execute(query)
        test = cursor.fetchall()
    if len(resultaat_kolommen) != 0:
        query = "select {} from Seq_Blast join Seq_Read SR on Seq_Blast.Blast_ID = SR.Read_ID " \
                "join Eiwitten E on Seq_Blast.Blast_ID = E.Prot_ID".format(" , ".join(resultaat_kolommen))
        cursor.execute(query)
        test = cursor.fetchall()
    if len(resultaat_kolommen) != 0 and len(resultaat_where) != 0:
        query = "select {} from Seq_Blast join Seq_Read SR on Seq_Blast.Blast_ID = SR.Read_ID join Eiwitten E on " \
                "Seq_Blast.Blast_ID = E.Prot_ID {}" \
            .format(" , ".join(resultaat_kolommen), " and ".join(resultaat_where))
        cursor.execute(query)
        test = cursor.fetchall()
    cursor.close()
    verbinding.close()
    if len(resultaat_kolommen) == 0:
        return render_template('results.html', data=test, lijst=lijst_kolommen)
    if len(resultaat_kolommen) != 0:
        return render_template('results.html', data=test, lijst=resultaat_kolommen)



@app.route('/organism')
def organisms():
    connection = mysql.connector.connect(host="remotemysql.com",
                                         user="rp5DHKQnCe",
                                         db="rp5DHKQnCe",
                                         password="enSHvniY78")
    cur = connection.cursor()
    cur.execute(
        "select distinct Organisme from Seq_Blast")

    data = cur.fetchall()
    return render_template('organism.html', data=data)


@app.route('/protein')
def protein():
    connection = mysql.connector.connect(host="remotemysql.com",
                                         user="rp5DHKQnCe",
                                         db="rp5DHKQnCe",
                                         password="enSHvniY78")
    cur = connection.cursor()
    cur.execute(
        "select distinct Prot_naam from Eiwitten")

    data = cur.fetchall()
    return render_template('protein.html', data=data)


@app.route('/blast')
def blast():
        """" Deze functie gaat controleren of de opgegeven sequentie een DNA, RNA of eiwit sequentie is. Als de sequentie
        DNA is, wordt de bijbehordende RNA en eiwit sequentie gegeven, is de sequentie een eiwit. Wordt het organisme
        waar de sequentie het meest op lijkt getoond. Als de sequentie geen DNA, RNA of eiwit is wordt het aangegeven
        met een bericht dat het geen van beide is. Dit allemaal wordt weergegeven op een HTML pagina
        """
        sequentie = request.args.get("seq")
        dna = False
        rna = False
        eiwit = False
        rotzooi = False
        titel = ''
        resultaat = ''


        if sequentie is not None:
            if len(re.findall("[ATCG]", sequentie, flags=re.IGNORECASE)) == len(sequentie):
                dna = True
            elif len(re.findall("[AUCG]", sequentie, flags=re.IGNORECASE)) == len(sequentie):
                rna = True
            elif len(re.findall("[ARNDCFQEGHILKMPSTWYV]", sequentie, flags=re.IGNORECASE)) == len(sequentie):
                eiwit = True
            else:
                rotzooi = True

        if dna is True:
            resultaat = "De opgegeven sequentie is DNA"
        elif rna is True:
            resultaat = "De opgegeven sequentie is RNA"
        elif eiwit is True:
            resultaat = "De opgegeven sequentie is eiwit"
        elif rotzooi is True:
            resultaat = "De opgegeven sequentie is geen DNA, RNA of eiwit sequentie"

        if sequentie is None:
            sequentie = ''
        if dna is True:
            result_handle = NCBIWWW.qblast("tblastx", "nr", str(sequentie))
            bestand = open("Resultaat_tblastx.xml", "w")
            resultaat_xml = result_handle.readlines()
            bestand.writelines(resultaat_xml)
            bestand.close()

            result_handle = open("Resultaat_tblastx.xml", "r")
            blast_records = NCBIXML.parse(result_handle)
            blast_record = next(blast_records)
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    titel = alignment.title
                    titels = titel.split("[")
                    titelss = titels[1].split("]")
                    titel = "Blast organisme: " + titelss[0]
                    break
            if dna is True and titel == '':
                titel = "Er is geen match gevonden met de dna sequentie: {}".format(sequentie)
        if eiwit is True:
            result_handle = NCBIWWW.qblast("blastx", "nr", str(sequentie))
            bestand = open("Resultaat_blastx.xml", "w")
            resultaat_xml = result_handle.readlines()
            bestand.writelines(resultaat_xml)
            bestand.close()

            result_handle = open("Resultaat_blastx.xml", "r")
            blast_records = NCBIXML.parse(result_handle)
            blast_record = next(blast_records)
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    titel = alignment.title
                    titels = titel.split("[")
                    titelss = titels[1].split("]")
                    titel = "Blast organisme: " + titelss[0]
                    break
            if eiwit is True and titel == '':
                titel = "Er is geen match gevonden met de eiwit sequentie: {}".format(sequentie)

        return render_template('BLAST.html', sequentie=sequentie, resultaat=resultaat, titel=titel)


if __name__ == '__main__':
    app.run()
