from flask import Flask, render_template,request
import mysql.connector
app = Flask(__name__)


@app.route('/', methods=['get','post'])
def home():
    return render_template('Database_page2.html')

@app.route('/results')
def results():
    connection = mysql.connector.connect(host="remotemysql.com",
                                         user="rp5DHKQnCe",
                                         db="rp5DHKQnCe",
                                         password="enSHvniY78")
    cur = connection.cursor()
    cur.execute(
        "select * from Eiwitten ")

    data = cur.fetchall()
    return render_template('results.html', data=data)

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
if __name__ == '__main__':
    app.run()
