import mysql.connector


def main():
    content = openfile()
    conn, cursor = connectie()
    vullen(content, conn, cursor)


def openfile():
    """Het bestand met de resultaten wordt geopend en gelezen, de lijnen
    worden gesplitst en deze content wordt gereturned
    """
    with open('nieuwblastxtblastxfilter.txt') as f:
        content = f.read().splitlines()
    return content


def connectie():
    """Er wordt een connectie gelegd met de database. De connector en de
    cursor worden gereturned.
    """
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="lszlh@hannl-hlo-bioinformatica-mysqlsrv",
        db="lszlh", password="619150")
    cursor = conn.cursor()
    return conn, cursor


def vullen(content, conn, cursor):
    """De content, connector en de cursor worden meegegeven. Voor elke
    hit wordt er gecontroleerd of die hit een header bevat. Als
    deze een header bevat gaat het ID met 1 omhoog. Als deze geen header
    bevat krijgt de hit dezelfde ID als de hit met de header. Voor elke hit
    worden de waarden en scores eruit gehaald. Elke tabel in de database
    wordt gevuld met bijbehorende waarden en een ID voor elke rij.
    """
    count = 0
    count2 = 0
    resultlijst = []
    ID = 0
    ID2 = 0
    headercount = 0
    teller = 0
    teller2 = 0

    for line in content:
        count += 1

    for i in range(0, count):

        resultlijst.append(content[count2])
        if '@' in content[i]:
            teller2 += 1
        header = resultlijst[0]
        count2 += 1
        if len(resultlijst) == 7:
            teller += 1
        if len(resultlijst) == 9:
            if 'P' in resultlijst[8]:
                for i in header:
                    headercount += 1
                header = resultlijst[0]
                seq = resultlijst[1]

                if teller2 < 172:
                    eiwitnaam1 = resultlijst[3].split("[")
                    organisme1 = resultlijst[3].split("[")
                Accessiecode1 = resultlijst[4].split(":")
                Score1 = resultlijst[5].split(":")
                Evalue1 = resultlijst[6].split(":")
                cover1 = resultlijst[7].split(":")
                Identity1 = resultlijst[8].split(":")
                resultlijst = []
                ID += 1
                q = header[headercount-1]

                if teller2 >= 172:
                    organisme2 = resultlijst[3].split(",")

                if q == '2':
                    cursor.execute(
                        "insert into seq_read(Read_ID,Read_type,"
                        "Header,Sequentie)VALUES (%s,2,'%s',"
                        "'%s')" % (ID, header, seq))
                    conn.commit()

                if q == '1':
                    cursor.execute("insert into seq_read(Read_ID,"
                                   "Read_type,Header,Sequentie)VALUES (%s,1,"
                                   "'%s','%s')" % (ID, header, seq))
                    conn.commit()
                headercount = 0

                if teller2 < 172:
                    cursor.execute(
                        "insert into blast(Blast_ID,Blast_type,"
                        "Organisme,Accessiecode,Score,E_value,Query_cover,"
                        "Percent_ident,Taxonomie,Actual_ID"
                        ")VALUES (%s,'blastx','%s','%s',%s,%s,%s,%s,"
                        "'-',%s)" % (
                            ID, organisme1[1], Accessiecode1[1], Score1[1],
                            Evalue1[1], cover1[1], Identity1[1], ID2))
                    conn.commit()

                if teller2 >= 172:
                    cursor.execute(
                        "insert into blast(Blast_ID,Blast_type,"
                        "Organisme,Accessiecode,Score,E_value,Query_cover,"
                        "Percent_ident,Taxonomie,Actual_ID"
                        ")VALUES ("
                        "%s,'tblastx','-','%s',%s,%s,"
                        "%s,"
                        "%s,'-',%s)" % (
                            ID, Accessiecode1[1], Score1[1], Evalue1[1],
                            cover1[1], Identity1[1], ID2))
                    conn.commit()

                if teller2 < 172:
                    cursor.execute(
                        "insert into eiwitten(Prot_id,Prot_naam,"
                        "Prot_locatie,Bio_domein,Bio_proces,"
                        "Bio_functie)VALUES(%s,'%s','-','-','-','-')" % (
                            ID2, eiwitnaam1[0]))
                    conn.commit()

                if teller2 >= 172:
                    cursor.execute(
                        "insert into eiwitten(Prot_id,Prot_naam,"
                        "Prot_locatie,Bio_domein,Bio_proces,Bio_functie"
                        ")VALUE (%s,'-','-','-','-','-')" % (ID2))
                    conn.commit()
                ID2 += 1

        if len(resultlijst) == 7:
            if 'P' in resultlijst[6]:
                if teller2 < 172:
                    eiwitnaam = resultlijst[1].split("[")
                    organisme = resultlijst[1].split("[")
                Accessiecode = resultlijst[2].split(":")
                Score = resultlijst[3].split(":")
                Evalue = resultlijst[4].split(":")
                cover = resultlijst[5].split(":")
                Identity = resultlijst[6].split(":")
                resultlijst = []

                if teller2 < 172:
                    cursor.execute(
                        "insert into blast(Blast_ID,Blast_type,"
                        "Organisme,Accessiecode,Score,E_value,Query_cover,"
                        "Percent_ident,Taxonomie,Actual_ID"
                        ")VALUES ("
                        "%s,'blastx','%s','%s',%s,%s,%s,"
                        "'%s','-',%s)" % (
                            ID, organisme[1], Accessiecode[1], Score[1],
                            Evalue[1], cover[1], Identity[1], ID2))
                    conn.commit()
                if teller2 >= 172:
                    cursor.execute(
                        "insert into blast(Blast_ID,Blast_type,"
                        "Organisme,Accessiecode,Score,E_value,Query_cover,"
                        "Percent_ident,Taxonomie,Actual_ID"
                        ")VALUES ("
                        "%s,'tblastx','%s','%s',%s,%s,"
                        "%s,"
                        "%s,'-',%s)" % (ID, organisme2[0], Accessiecode[1],
                                        Score[1], Evalue[1], cover[1],
                                        Identity[1], ID2))
                    conn.commit()

                if teller2 < 172:
                    cursor.execute(
                        "insert into eiwitten(Prot_id,Prot_naam,"
                        "Prot_locatie,Bio_domein,Bio_proces,"
                        "Bio_functie"
                        ")VALUES ("
                        "%s,'%s','-','-','-','-')" % (ID2, eiwitnaam[0]))
                    conn.commit()

                if teller2 >= 172:
                    cursor.execute(
                        "insert into eiwitten(Prot_id,Prot_naam,"
                        "Prot_locatie,Bio_domein,Bio_proces,Bio_functie"
                        ")VALUE ("
                        "%s,'-','-','-','-','-')" % (ID2))
                    conn.commit()
                ID2 += 1

    conn.close()


main()
