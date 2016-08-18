import os
import psycopg2
from flask import Flask, render_template
import urlparse
import logging
from logging.handlers import RotatingFileHandler
from flask import request

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
schema = "schema.sql"
conn = psycopg2.connect(db)

cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    #return 'Hello World!'
    return render_template('home.html')

@app.route('/contactform')
def contactform():
   return render_template('contactform.html')

@app.route('/contacts')
def contacts():
    try:
        cur.execute("""SELECT name from salesforce.contact""")
        rows = cur.fetchall()
        response = ''
        my_list = []
        for row in rows:
            my_list.append(row[0])

        return render_template('contact_list.html',  results=my_list)
    except Exception as e:
        print(e)
        return []

@app.route('/create_contact', methods=['POST','GET'])
def create_contact():

    try:
        if request.method == "POST":
            first_name = request.form["first-name"]
            last_name = request.form["last-name"]
            email = request.form["email"]

            app.logger.info(first_name)
            statement = "insert into salesforce.contact(firstname, lastname, email) values ('" \
                + first_name + "','" + last_name + "','" + email + "');"
            cur.execute(statement)
            conn.commit()
            errors = []
            return render_template('result.html', errors=errors, firstname=first_name,
                                   lastname=last_name)
    except Exception as e:
        print(e)
        return []

    
if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()


