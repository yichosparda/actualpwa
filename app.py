from flask import Flask, render_template, request
import sqlite3
import bcrypt
s = bcrypt.gensalt()

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('index.html')

def insert_acc(email, username, password):
    if email is None or username is None or password is None:
        return

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        # Use parameterized query to avoid SQL injection and handle values safely
        cursor.execute("INSERT INTO customers(email, username, password) VALUES (?,?,?)", (email,username,password))
        conn.commit()
        # cursor.execute("CREATE TABLE employees")
    # print("You are in insert_data ->", data)

def check_acc(email, password):
    if email is None or password is None:
        return

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM customers WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            # 3. If user doesn't exist, return False
            if not row:
                return False
            
            stored_password = row[0]
            
            # 4. Check if the provided password matches the stored hash
            # bcrypt handles the salt automatically during comparison
            if password == stored_password:
                return True
            else:
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

@app.route('/menu')

def menu():

    return render_template('menu.html')

@app.route('/custom')

def custom():

    return render_template('custom.html')

@app.route('/signup', methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = bcrypt.hashpw((request.form.get('password').encode()),s)
        # print("The data is", data)
        # print(email)
        # print(username)
        # print(password)
        insert_acc(email, username, password)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = bcrypt.hashpw((request.form.get('password').encode()),s)
        # print("The data is", data)
            # insert_data(data)
        if check_acc(email,password):
            print("logged in!")
        else: print("email or password is wrong")

    return render_template('login.html')

@app.route('/manifest.json')

def manifest():

    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')

def service_worker():

    return app.send_static_file('service-worker.js')

if __name__ == '__main__':

    app.run(debug=True)