from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('index.html')

def insert_data(data):
    if data is None:
        return

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        # Use parameterized query to avoid SQL injection and handle values safely
        cursor.execute("INSERT INTO accounts (email) VALUES (?)", (data,))
        conn.commit()

    # print("You are in insert_data ->", data)

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    # Only insert when the form is submitted via POST and a value is provided
    if request.method == 'POST':
        data = request.form.get('data')
        # print("The data is", data)
        if data:
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