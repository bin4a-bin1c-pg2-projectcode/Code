from Bio import Entrez, SeqIO
import mysql.connector
import time
import urllib.error


def main():
    accessiecodes_blastx, accessiecodes_tblastx = database_gegevens()
    taxonomy_blastx(accessiecodes_blastx)
    taxonomy_tblastx(accessiecodes_tblastx)
    database_blastx()
    database_tblastx()
    inserten_blastx()
    inserten_tblastx()
    resultaten_geenhitstblastx()
    database_geenhitsblastx()
    inserten_geenhitsblastx()
    resultaten_geenhitsblastx()
    database_geenhitsblastx()
    inserten_geenhitsblastx()


def database_gegevens():
    """ deze functie maakt de connectie met de database en voert 2x een query uit. De eerste query is accessiecodes voor
    blastx en daarna voor accessiecodes van tblastx. Deze worden in 2 aparte lijsten gezet en deze worden gereturnd.

    :return lijst accessiecodes blastx
    :return lijst accessiecodes tblastx
    """
    accessiecodes_blastx = []
    accessiecodes_tblastx = []
    verbinding = mysql.connector.connect(host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
                                         user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
                                         db="lszlh",
                                         passwd="619150")
    cursor = verbinding.cursor()
    query_blastx = "select Accessiecode from blast where Blast_type = 'blastx'"
    query_tblastx = "select Accessiecode from blast where Blast_type = 'tblastx'"
    cursor.execute(query_blastx)
    resultaat_blastx = cursor.fetchall()
    for resultaat in resultaat_blastx:
        restultaatt = "".join(resultaat)
        accessiecodes_blastx.append(restultaatt)
    cursor.execute(query_tblastx)
    resultaat_tblastx = cursor.fetchall()
    for resultaat in resultaat_tblastx:
        restultaatt = "".join(resultaat)
        accessiecodes_tblastx.append(restultaatt)

    return accessiecodes_blastx, accessiecodes_tblastx


def taxonomy_blastx(accessiecodes_blastx):
    """ Deze functie opent 2 bestanden, een bestand waar de taxonomie wordt opgeslagen en een bestand waarin
    accessiecodes staan die geen resultaat hebben opgeleverd. De functie krijgt ook de lijst accessiecodes_blastx mee.
    Met behulp van Entrez wordt elke accessiecode in de lijst gezocht naar de taxonomie in de protein database,
    en wordt met SeqIO uitgelezen en weggeschreven naar een bestand. Over dit hangt een try en except, als er een error
    optreedt, wordt de accessiecode in het andere bestand geschreven.

    :param accessiecodes_blastx, lijst met alle accessiecodes van blastx
    :return bestand met alle taxonomie
    :return bestand met accessiecodes waar geen taxonomie is gevonden
    """
    bestand = open('taxonomy_blastx.txt', 'w')
    bestand_2 = open('fouten-taxonomy_blastx.txt', 'w')
    Entrez.email = 'inge1vugt@gmail.com'
    for item in accessiecodes_blastx:
        try:
            time.sleep(5)
            print("Begin met zoeken", accessiecodes_blastx.index(item), "van de", len(accessiecodes_blastx))
            handle = Entrez.efetch(db="protein", id=item, rettype="gb", retmode="text")
            uitlezen = SeqIO.read(handle, 'genbank')
            bestand.write(str(uitlezen))
            print("Klaar met zoeken")
        except urllib.error.HTTPError:
            bestand_2.write(item)
            bestand_2.write("\n")


def taxonomy_tblastx(accessiecodes_tblastx):
    """ Deze functie opent 2 bestanden, een bestand waar de taxonomie wordt opgeslagen en een bestand waarin
    accessiecodes staan die geen resultaat hebben opgeleverd. De functie krijgt ook de lijst accessiecodes_tblastx mee.
    Met behulp van Entrez wordt elke accessiecode in de lijst gezocht naar de taxonomie in de protein database,
    en wordt met SeqIO uitgelezen en weggeschreven naar een bestand. Over dit hangt een try en except, als er een error
    optreedt, wordt de accessiecode in het andere bestand geschreven.

    :param accessiecodes_tblastx, lijst met alle accessiecodes van tblastx
    :return bestand met alle taxonomie
    :return bestand met accessiecodes waar geen taxonomie is gevonden
    """
    bestand = open('taxonomy_tblastx.txt', 'w')
    bestand_2 = open('fouten-taxonomy_tblastx.txt', 'w')
    Entrez.email = 'inge1vugt@gmail.com'
    for item in accessiecodes_tblastx:
        try:
            time.sleep(5)
            print("Begint met zoeken", accessiecodes_tblastx.index(item), "van de ", len(accessiecodes_tblastx))
            print(item)
            handle = Entrez.efetch(db="nucleotide", id=item, rettype="gb", retmode="text")
            uitlezen = SeqIO.read(handle, 'genbank')
            bestand.write(str(uitlezen))
            print("Klaar met zoeken")
        except urllib.error.HTTPError:
            bestand_2.write(str(item))
            bestand_2.write("\n")
    bestand.close()
    bestand_2.close()


def database_blastx():
    """ Deze functie opent 2 bestanden, het ene bestand met alle taxonomie en een leeg bestand. Voor elke resultaat
    wordt de accessiecode, naam organisme en de taxonomie eruit gehaald en in een ander bestand geschreven om het later
    zo toe te kunnen voegen in de database.

    :return tekstbestand voor de database, elk resultaat bevat de accessiecode, taxonomie en naam organisme
    """
    bestand = open('taxonomy_blastx.txt', 'r')
    bestand2 = open('database_blastx.txt', 'w')

    for regel in bestand:
        regel1 = regel.replace("\n", "")
        regel2 = str(regel1)
        if regel2.startswith("/accessions="):  # hier bevindt zich de accessiecode
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(" ")
            bestand2.write(str(regel6))
            bestand2.write("\n")
        if regel2.startswith("Description:"):  # hier bevindt zich het organisme naam met eiwit
            regel3 = regel2.split(": ")
            bestand2.write(str(regel3[1]))
            bestand2.write("\n")
        if regel2.startswith("/taxonomy="):  # hier bevindt zich de taxonomie
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(regel6)
            bestand2.write("\n" + "\n")

    bestand.close()
    bestand2.close()


def database_tblastx():
    """ Deze functie opent 2 bestanden, het ene bestand met alle taxonomie en een leeg bestand. Voor elke resultaat
    wordt de accessiecode, naam organisme en de taxonomie eruit gehaald en in een ander bestand geschreven om het later
    zo toe te kunnen voegen in de database.

    :return tekstbestand voor de database, elk resultaat bevat de accessiecode, taxonomie en naam organisme
    """
    bestand = open('taxonomy_tblastx.txt', 'r')
    bestand2 = open('database_tblastx.txt', 'w')

    for regel in bestand:
        regel1 = regel.replace("\n", "")
        regel2 = str(regel1)
        if regel2.startswith("/accessions="):  # hier bevindt zich de accessiecode
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(" ")
            bestand2.write(str(regel6))
            bestand2.write("\n")
        if regel2.startswith("Description:"):  # hier bevindt zich het organisme naam
            regel3 = regel2.split(": ")
            bestand2.write(str(regel3[1]))
            bestand2.write("\n")
        if regel2.startswith("/taxonomy="):  # hier bevindt zich de taxonomie
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(regel6)
            bestand2.write("\n" + "\n")

    bestand.close()
    bestand2.close()


def inserten_tblastx():
    """ Deze functie opent het bestand waarin de gegevens staan van de database. Hij legt connectie aan met de database
    en gaat dan voor elke regel in het bestand kijken, als het een accessiecode en taxonomie heeft, wordt deze
    geupdate in de database.

    :return: taxonomie toevoegingen in de database
    """
    bestand = open('database_tblastx.txt', 'r')
    verbinding = mysql.connector.connect(host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
                                         user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
                                         db="lszlh",
                                         passwd="619150")
    cursor = verbinding.cursor()
    count = 0
    for regel in bestand:
        regel = regel.replace("\n", '')
        count += 1
        if count == 1:
            accessiecode = str(regel)
        if count == 3:
            taxonomie = regel
        if count == 4:
            print("Begint met updaten")
            count = 0
            query = "update blast set Taxonomie = '{}' where Accessiecode = '{}'".format(taxonomie, accessiecode)
            cursor.execute(query)
            verbinding.commit()
            print("Gestopt met updaten")
    bestand.close()


def inserten_blastx():
    """ Deze functie opent het bestand waarin de gegevens staan van de database. Hij legt connectie aan met de database
    en gaat dan voor elke regel in het bestand kijken, als het een accessiecode en taxonomie heeft, wordt deze
    geupdate in de database.

    :return: taxonomie toevoegingen in de database
    """
    bestand = open('database_blastx.txt', 'r')
    verbinding = mysql.connector.connect(host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
                                         user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
                                         db="lszlh",
                                         passwd="619150")
    cursor = verbinding.cursor()
    count = 0
    for regel in bestand:
        regel = regel.replace("\n", '')
        count += 1
        if count == 1:
            accessiecode = str(regel)
        if count == 3:
            taxonomie = regel
        if count == 4:
            print("Begint met updaten")
            count = 0
            query = "update blast set Taxonomie = '{}' where Accessiecode = '{}'".format(taxonomie, accessiecode)
            cursor.execute(query)
            verbinding.commit()
            print("Gestopt met updaten")

    bestand.close()


def resultaten_geenhitstblastx():
    """ Deze functie opent het bestand waarin de eventuele accessiecodes staan waar geen hit op is gevonden. Deze worden
    nog een keer gezocht in de nucleotide database. De try en except schrijft weer een bestand weg als er geen resultaat
    gevonden is, als er wel een resultaat gevonden is, wordt deze in een ander bestand weggeschreven

    :return bestand met taxonomie
    :return bestand met accessiecodes waar geen resultaat voor is gevonden
    """
    bestand = open('fouten-taxonomy_tblastx.txt', 'r')
    bestand_2 = open('geenhits_tblastx.txt', 'w')
    Entrez.email = 'inge1vugt@gmail.com'

    for regel in bestand:
        try:
            regel = regel.replace("\n", '')
            regel = regel.replace(" ", "")
            handle = Entrez.efetch(db="nucleotide", id=regel, rettype="gb", retmode="text")
            uitlezen = SeqIO.read(handle, 'genbank')
            bestand_2.write(str(uitlezen))
        except urllib.error.HTTPError:
            bestand_2.write(regel)
            bestand_2.write("\n")
    bestand.close()
    bestand_2.close()


def database_geenhitstblastx():
    """ Deze functie opent 2 bestanden, het ene bestand met alle taxonomie en een leeg bestand. Voor elke resultaat
    wordt de accessiecode, naam organisme en de taxonomie eruit gehaald en in een ander bestand geschreven om het later
    zo toe te kunnen voegen in de database.

    :return tekstbestand voor de database, elk resultaat bevat de accessiecode, taxonomie en naam organisme
    """
    bestand = open('geenhits_tblastx.txt', 'r')
    bestand2 = open('resultatengeenhits_tblastx.txt', 'w')

    for regel in bestand:
        regel1 = regel.replace("\n", "")
        regel2 = str(regel1)
        if regel2.startswith("/accessions="):  # hier bevindt zich de accessiecode
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(" ")
            bestand2.write(str(regel6))
            bestand2.write("\n")
        if regel2.startswith("Description:"):  # hier bevindt zich het organisme naam
            regel3 = regel2.split(": ")
            bestand2.write(str(regel3[1]))
            bestand2.write("\n")
        if regel2.startswith("/taxonomy="):  # hier bevindt zich de taxonomie
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(regel6)
            bestand2.write("\n" + "\n")

    bestand.close()
    bestand2.close()


def inserten_geenhitstblastx():
    """ Deze functie opent het bestand waarin de gegevens staan van de database. Hij legt connectie aan met de database
    en gaat dan voor elke regel in het bestand kijken, als het een accessiecode en taxonomie heeft, wordt deze
    geupdate in de database.

    :return: taxonomie toevoegingen in de database
    """
    bestand = open('resultatengeenhits_tblastx.txt', 'r')
    verbinding = mysql.connector.connect(host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
                                         user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
                                         db="lszlh",
                                         passwd="619150")
    cursor = verbinding.cursor()
    count = 0
    for regel in bestand:
        regel = regel.replace("\n", '')
        count += 1
        if count == 1:
            accessiecode = str(regel)
        if count == 3:
            taxonomie = regel
        if count == 4:
            print("Begint met updaten")
            count = 0
            query = "update blast set Taxonomie = '{}' where Accessiecode = '{}'".format(taxonomie, accessiecode)
            cursor.execute(query)
            verbinding.commit()
            print("Gestopt met updaten")
    bestand.close()


def resultaten_geenhitsblastx():
    """ Deze functie opent het bestand waarin de eventuele accessiecodes staan waar geen hit op is gevonden. Deze worden
    nog een keer gezocht in de protein database. De try en except schrijft weer een bestand weg als er geen resultaat
    gevonden is, als er wel een resultaat gevonden is, wordt deze in een ander bestand weggeschreven

    :return bestand met taxonomie
    :return bestand met accessiecodes waar geen resultaat voor is gevonden
    """
    bestand = open('fouten-taxonomy_blastx.txt', 'r')
    bestand_2 = open('geenhits_blastx.txt', 'w')
    Entrez.email = 'inge1vugt@gmail.com'

    for regel in bestand:
        try:
            regel = regel.replace("\n", '')
            regel = regel.replace(" ", "")
            handle = Entrez.efetch(db="protein", id=regel, rettype="gb", retmode="text")
            uitlezen = SeqIO.read(handle, 'genbank')
            bestand_2.write(str(uitlezen))
        except urllib.error.HTTPError:
            bestand_2.write(regel)
            bestand_2.write("\n")
    bestand.close()
    bestand_2.close()


def database_geenhitsblastx():
    """ Deze functie opent 2 bestanden, het ene bestand met alle taxonomie en een leeg bestand. Voor elke resultaat
    wordt de accessiecode, naam organisme en de taxonomie eruit gehaald en in een ander bestand geschreven om het later
    zo toe te kunnen voegen in de database.

    :return tekstbestand voor de database, elk resultaat bevat de accessiecode, taxonomie en naam organisme
    """
    bestand = open('geenhits_blastx.txt', 'r')
    bestand2 = open('resultatengeenhits_blatx.txt', 'w')

    for regel in bestand:
        regel1 = regel.replace("\n", "")
        regel2 = str(regel1)
        if regel2.startswith("/accessions="):  # hier bevindt zich de accessiecode
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(" ")
            bestand2.write(str(regel6))
            bestand2.write("\n")
        if regel2.startswith("Description:"):  # hier bevindt zich het organisme naam en eiwit
            regel3 = regel2.split(": ")
            bestand2.write(str(regel3[1]))
            bestand2.write("\n")
        if regel2.startswith("/taxonomy="):  # hier bevindt zich de taxonomie
            regel3 = regel2.split("=")
            regel4 = regel3[1].replace("'", "")
            regel5 = regel4.replace("[", "")
            regel6 = regel5.replace("]", "")
            bestand2.write(regel6)
            bestand2.write("\n" + "\n")

    bestand.close()
    bestand2.close()


def inserten_geenhitsblastx():
    """ Deze functie opent het bestand waarin de gegevens staan van de database. Hij legt connectie aan met de database
    en gaat dan voor elke regel in het bestand kijken, als het een accessiecode en taxonomie heeft, wordt deze
    geupdate in de database.

    :return: taxonomie toevoegingen in de database
    """
    bestand = open('resultatengeenhits_blatx.txt', 'r')
    verbinding = mysql.connector.connect(host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
                                         user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
                                         db="lszlh",
                                         passwd="619150")
    cursor = verbinding.cursor()
    count = 0
    for regel in bestand:
        regel = regel.replace("\n", '')
        count += 1
        if count == 1:
            accessiecode = str(regel)
        if count == 3:
            taxonomie = regel
        if count == 4:
            print("Begint met updaten")
            count = 0
            query = "update blast set Taxonomie = '{}' where Accessiecode = '{}'".format(taxonomie, accessiecode)
            cursor.execute(query)
            verbinding.commit()
            print("Gestopt met updaten")
    bestand.close()


main()

# cdd
