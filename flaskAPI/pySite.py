import psycopg2
import requests
import configparser

from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy


#adds data from postgres weatherdata table
def add_data(zipcode, temperature):
    con = psycopg2.connect(
        dbname = 'postgres',
        host='localhost',
        user = 'postgres',
        password = 'mypassword'
    )

    cur = con.cursor()

    #cur.execute("CREATE TABLE weatherData ( id SERIAL PRIMARY KEY, zip VARCHAR, temp INTEGER);")

    cur.execute("INSERT INTO weatherData (zip, temp) VALUES (%s,%s)", (zipcode, temperature))

    con.commit()

    cur.close()
    con.close()

#shows data from postgres weatherdata table
def show_data():
    con = psycopg2.connect(
        dbname = 'postgres',
        host='localhost',
        user = 'postgres',
        password = 'mypassword'
    )

    cur = con.cursor()

    cur.execute("SELECT * FROM weatherData;")

    print(cur.fetchall())

    con.commit()

    cur.close()
    con.close()


#gets api key from config.ini
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_data(zip, api_key):
    api_url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}'.format(zip, api_key)
    r = requests.get(api_url)
    return r.json()

def delete_all():
    con = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="localhost", port="5432")
    cur = con.cursor()

    cur.delete('DELETE FROM weatherData;')
    



app = Flask(__name__)

con = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="localhost", port="5432")
cur = con.cursor()

@app.route("/")
def weather_home():
    return render_template("index.html")


@app.route('/results', methods=['POST', 'GET'])
def render_results():
    zip = request.form['zipcode']

    api_key = get_api_key()
    data = get_weather_data(zip, api_key)
    temp = (data["main"]["temp"])
    location = data["name"]

    cur.execute("select * from weatherData")
    result = cur.fetchall()

    return render_template('results.html', location=location, temp=temp, data=result),  add_data(zip, temp), show_data()

    


if __name__ == "__main__":
    app.run()






