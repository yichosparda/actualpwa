from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('index.html')

def insert_data(data):

    with sqlite3.connect("myDB.db") as conn:

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO myTable (myFirstCol) VALUES ('{data}')")

        conn.commit()

    print("You are in insert_data - > ", data)

@app.route('/page1', methods=['GET', 'POST'])

def page1():

    data = request.form.get('data')

    print("The data is", data)

    insert_data(data)  # Insert the data into the database

    return render_template('page1.html')

@app.route('/menu')

def menu():

    return render_template('menu.html')

@app.route('/custom')

def custom():

    return render_template('custom.html')

@app.route('/account')

def account():

    return render_template('account.html')

@app.route('/manifest.json')

def manifest():

    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')

def service_worker():

    return app.send_static_file('service-worker.js')

if __name__ == '__main__':

    app.run(debug=True)