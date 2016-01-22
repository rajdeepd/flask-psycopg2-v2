import os
import psycopg2
from flask import Flask, render_template
import urlparse
from os.path import exists
from os import makedirs
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
def hello():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return 'Hello World!'

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

        return render_template('template.html',  results=my_list)
    except Exception as e:
        print e
        return []

@app.route('/create_contact', methods=['POST','GET'])
def create_contact():

    try:
        if request.method == "POST":
		firstname = request.form["first-name"]
                lastname = request.form["last-name"]
                email = request.form["email"]
		
		app.logger.info(firstname)
		statement = "insert into salesforce.contact(firstname, lastname, email) values ('" \
		    + firstname + "','" + lastname +  "','" + email + "');"
		cur.execute(statement)
		conn.commit()
		errors = []
		results = {'A':'1','B':'2'}
		return render_template('result.html', errors=errors, firstname=firstname, 
			lastname= lastname)
    except Exception as e:
        print e
        return []

    
if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()

	
