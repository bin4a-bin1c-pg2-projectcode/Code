from flask import Flask, render_template,request
import mysql.connector
from Bio.Seq import Seq, transcribe
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
    lijst_organisme = ["organisme", "eiwit", "checkboxread1", "checkboxread2", "checkboxread3",
                       "checkboxblastx", "checkboxtblastx", "checkboxboth"]
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
        index_getal = lijst_organisme.index(item)
        result = request.form.get(item)
        if result is not None:
            if len(result) > 0:
                if index_getal == 0:
                    resultaat_where.append("where Organisme like '%{}%'".format(result))
                if index_getal == 1:
                    if len(resultaat_where) > 1:
                        resultaat_where.append("Prot_naam like '%{}%'".format(result))
                    elif len(resultaat_where) == 0:
                        resultaat_where.append("where Prot_naam like '%{}%'".format(result))
            if index_getal == 2 or index_getal == 3 or index_getal == 4:
                if len(resultaat_where) > 0:
                    resultaat_where.append("Read_type = {}".format(result))
                if len(resultaat_where) == 0:
                    resultaat_where.append("where Read_type = {}".format(result))
            if index_getal == 5 or index_getal == 6 or index_getal == 7:
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
        query = "select {} from Seq_Blast join Seq_Read SR on Seq_Blast.Blast_ID = SR.Read_ID join Eiwitten E on " \
                "Seq_Blast.Blast_ID = E.Prot_ID {}" \
            .format(" , ".join(lijst_kolommen), " and ".join(resultaat_where))
        cursor.execute(query)
        test = cursor.fetchall()
    if len(resultaat_kolommen) != 0:
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
        anders = False
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
                anders = True

        if dna is True:
            resultaat = "The sequence is DNA"
        elif rna is True:
            resultaat = "The sequence is RNA"
        elif eiwit is True:
            resultaat = "The sequence is eiwit"
        elif anders is True:
            resultaat = "The sequence is not DNA, RNA or protein"

        blast_resultaat = []
        if dna is True:
            sequentie = request.args.get("seq")
            blast_type = request.args.get("blast_type")
            if sequentie is not None and blast_type == "blastx":
                bestand = open("Resultaat.xml", "w")
                result_handle = NCBIWWW.qblast("blastx", "nr", sequentie)
                bestand.write(result_handle.getvalue())
                bestand.close()

                result_handle = open("Resultaat.xml", "r")
                blast_records = NCBIXML.parse(result_handle)
                blast_record = next(blast_records)
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        blast_resultaat.append("****Alignment****")
                        titel = alignment.title
                        titels = titel.split("[")
                        titelss = titels[1].split("]")
                        titel_ = titel.split("|")
                        titel__ = titel_[2].split("[")
                        blast_resultaat.append("Blast organism: {}".format(titelss[0]))
                        blast_resultaat.append("Protein: {}".format(titel__[0]))
                        blast_resultaat.append("Sequence: {}".format(alignment.title))
                        blast_resultaat.append("Length: {}".format(alignment.length))
                        blast_resultaat.append("E-value: {}".format(hsp.expect))
                        blast_resultaat.append(hsp.query[0:75] + "...")
                        blast_resultaat.append(hsp.match[0:75] + "...")
                        blast_resultaat.append(hsp.sbjct[0:75] + "...")
                        blast_resultaat.append("\n")
            if sequentie is not None and blast_type == "tblastx":
                bestand = open("Resultaat.xml", "w")
                result_handle = NCBIWWW.qblast("tblastx", "nr", sequentie)
                print(result_handle.getvalue())
                bestand.write(result_handle.getvalue())
                bestand.close()

                result_handle = open("Resultaat.xml", "r")
                blast_records = NCBIXML.parse(result_handle)
                blast_record = next(blast_records)
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        blast_resultaat.append("****Alignment****")
                        titel = alignment.title
                        titels = titel.split("|")
                        titel = "Blast organisme: " + titels[4]
                        blast_resultaat.append("Blast organisme: {}".format(titels[4]))
                        blast_resultaat.append("Sequence: {}".format(alignment.title))
                        blast_resultaat.append("Length: {}".format(alignment.length))
                        blast_resultaat.append("E-value: {}".format(hsp.expect))
                        blast_resultaat.append(hsp.query[0:75] + "...")
                        blast_resultaat.append(hsp.match[0:75] + "...")
                        blast_resultaat.append(hsp.sbjct[0:75] + "...")
                        blast_resultaat.append("\n")
            if titel == '':
                titel = "Er is geen match gevonden met de dna sequentie: {}".format(sequentie)
        titel = "\n".join(blast_resultaat)
        return render_template('BLAST.html', sequentie=sequentie, resultaat=resultaat, titel=titel)


if __name__ == '__main__':
    app.run()
