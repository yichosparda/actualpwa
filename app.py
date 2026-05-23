from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('index.html')

@app.route('/page1')

def page1():

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