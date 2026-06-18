from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3
import bcrypt
s = bcrypt.gensalt()

app = Flask(__name__)

app.secret_key = 'your_secret_key'

def get_db_connection():
    # Connects to your SQL database file
    conn = sqlite3.connect('myDB.db')
    # Configures the connection to return rows that act like dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def insert_acc(email, username, password):
    if email is None or username is None or password is None:
        return

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        # Use parameterized query to avoid SQL injection and handle values safely
        cursor.execute("INSERT INTO customers(email, username, password) VALUES (?,?,?)", (email,username,password))
        conn.commit()
        session['logged_in'] = True
        cursor.execute("SELECT cust_ID, username FROM customers WHERE email = ?", (email,))
        row = cursor.fetchone()
        session['ID'] = row[0]
        session['name'] = row[1]
        return render_template('cart.html', name = session['name'])
        print(session['ID'])
        # cursor.execute("CREATE TABLE employees")
    # print("You are in insert_data ->", data)

def check_acc(email, password):
    if email is None or password is None:
        return False

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM customers WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            # 3. If user doesn't exist, return False
            if not row:
                return False
            
            stored_password = row[0]
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8')
            
            # 4. Check if the provided password matches the stored hash
            if bcrypt.checkpw(password.encode(), stored_password):
                session['logged_in'] = True
                cursor.execute("SELECT cust_ID, username FROM customers WHERE email = ?", (email,))
                row = cursor.fetchone()
                session['ID'] = row[0]
                session['name'] = row[1]
                return render_template('cart.html', name = session['name'])
                print(session['ID'])
                return True
            else:
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

def insert_request(submission):
    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        # Use parameterized query to avoid SQL injection and handle values safely
        cursor.execute("INSERT INTO requests(cust_ID, request) VALUES (?,?)", (session['ID'], submission))
        conn.commit()

@app.route('/')

def home():

    return render_template('index.html')

@app.route('/menu')

def show_items():
    conn = get_db_connection()
    # Execute the SQL query to get all items
    cakes = conn.execute('SELECT product_name, price FROM products WHERE type="cake"').fetchall()
    pies = conn.execute('SELECT product_name, price FROM products WHERE type="pie"').fetchall()
    breads = conn.execute('SELECT product_name, price FROM products WHERE type="bread"').fetchall()
    cookies = conn.execute('SELECT product_name, price FROM products WHERE type="cookie"').fetchall()
    others = conn.execute('SELECT product_name, price FROM products WHERE type="other"').fetchall()
    conn.close()
    
    # Pass the database results to the HTML template as the variable "items"
    return render_template('menu.html', cakes=cakes, pies=pies, breads=breads, cookies=cookies, others=others)

@app.route('/product')
def product():
    name = request.args.get('name')
    print(name)
    return render_template('product.html', product=name)


@app.route('/custom', methods=['GET','POST'])

def custom():
    if request.method == 'POST':
        if 'logged_in' in session:
            submission=request.form.get('request')
            insert_request(submission)
        else:
            return redirect(url_for('signup'))
    return render_template('custom.html')

@app.route('/signup', methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt())
        insert_acc(email, username, password)
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if check_acc(email, password):
            print("logged in!")
            return redirect(url_for('home'))
        
        else:
            print("email or password is wrong")

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove all keys from the session dictionary
    session.clear()
    return redirect(url_for('login'))

@app.route('/cart')

def cart():
    if 'logged_in' in session:
        return render_template('cart.html', name=session['name'])
    else: 
        return render_template('signup.html')

@app.route('/manifest.json')

def manifest():

    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')

def service_worker():

    return app.send_static_file('service-worker.js')

if __name__ == '__main__':

    app.run(debug=True)