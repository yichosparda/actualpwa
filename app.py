from flask import Flask, render_template, session, request, redirect, url_for, flash
import sqlite3
import bcrypt
import bleach
s = bcrypt.gensalt()

app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,   # True if using HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)

def get_db_connection():
    # connects to SQL database file
    conn = sqlite3.connect('myDB.db')
    # return rows that act like dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def insert_acc(email, username, password):
    if email is None or username is None or password is None:
        return #cancel function if there isn't an email, username or password

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        # parameterized query to avoid SQL injection and handle values safely
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)", (email,))
        email_exists=cursor.fetchone()[0] 
        if email_exists:
            return None #cancel function if account under same email already exists
        
        else: #if email is unregistered
            cursor.execute("INSERT INTO users(email, username, password) VALUES (?,?,?)", (email,username,password))
            conn.commit() #create/add new account to database
            session['logged_in'] = True #start session
            cursor.execute("SELECT user_ID, username FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            session['ID'] = row[0] #assigns user ID to session
            session['name'] = row[1] #assigns username to session
            cursor.execute(f"CREATE TABLE IF NOT EXISTS '{session['ID']}_cart'(product_ID INTEGER REFERENCES products(product_ID), amount INTEGER NOT NULL)")
            conn.commit() #creates cart table for new user
            return redirect(url_for('cart', name=session['name']))

def check_acc(email, password):
    if email is None or password is None:
        return False #cancel function if there isn't an email or password

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
            row = cursor.fetchone() #selects row where email is the same
            
            if not row:
                return False #if there's no row with inputted email, cancel login
            
            stored_password = row[0] #selects the matching password for the respective email
            if isinstance(stored_password, str):
                stored_password = stored_password.encode('utf-8') #turns the password as a string
            
            if bcrypt.checkpw(password.encode(), stored_password): #checks if given and stored passwords are the same
                session['logged_in'] = True #creates session
                cursor.execute("SELECT user_ID, username FROM users WHERE email = ?", (email,))
                row = cursor.fetchone()
                session['ID'] = row[0]
                session['name'] = row[1]
                #same thing as creating account
                return True
            else:
                return False #cancels login/function if passwords don't match
                
        except sqlite3.Error as e: #failsafe
            print(f"Database error: {e}")
            return False

def insert_request(submission):
    submission = bleach.clean(
        submission,
        tags=[],
        attributes={},
        strip=True
    )

    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO requests(user_ID, request) VALUES (?, ?)",
            (session['ID'], submission)
        )
        conn.commit()

def insert_cart(pID, amount):
    with sqlite3.connect("myDB.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM '{session['ID']}_cart' WHERE product_ID = {pID})")
        item_exists=cursor.fetchone()[0]
        #checks if item is already in cart
        if item_exists:
            cursor.execute(f"UPDATE '{session['ID']}_cart' SET amount = amount+{amount} WHERE product_ID={pID}")
            conn.commit() #adds to quantity if item is already in cart
        else:
            cursor.execute(f"INSERT INTO '{session['ID']}_cart'(product_ID, amount) VALUES (?,?)", (pID, amount))
            conn.commit()  #creates new row/instance in cart/table if item does not exist yet

@app.route('/')

def home():

    return render_template('index.html')

@app.route('/menu')

def show_items():
    conn = get_db_connection()
    cakes = conn.execute('SELECT product_ID, product_name, price, ingredients, description FROM products WHERE type="cake"').fetchall()
    pies = conn.execute('SELECT product_ID, product_name, price, ingredients, description FROM products WHERE type="pie"').fetchall()
    breads = conn.execute('SELECT product_ID, product_name, price, ingredients, description FROM products WHERE type="bread"').fetchall()
    cookies = conn.execute('SELECT product_ID, product_name, price, ingredients, description FROM products WHERE type="cookie"').fetchall()
    others = conn.execute('SELECT product_ID, product_name, price, ingredients, description FROM products WHERE type="other"').fetchall()
    conn.close()
    #passing variables to html
    return render_template('menu.html', cakes=cakes, pies=pies, breads=breads, cookies=cookies, others=others)

@app.route('/product', methods=['GET', 'POST'])
def product():
    #receiving/processing variables passed from html
    pID = int(request.args.get('pID'))
    name = request.args.get('name')
    price = request.args.get('price')
    ingredients = request.args.get('ingredients')
    desc = request.args.get('desc')
    
    try: status = session['logged_in'] 
    except : status = False
    #determines whether or not user is logged in

    if request.method == 'POST':
        amount=request.form.get('quantity')
        insert_cart(pID, amount) #update cart
        return redirect(url_for('show_items'))

    return render_template('product.html', pID=pID, name=name, price=price, status=status, ingredients=ingredients, desc=desc)


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
        #receiving data from html
        email = request.form.get('email')
        username = request.form.get('username')
        password = bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt())
        #hashing password for security
        result= insert_acc(email, username, password) #try to create new account
        if result: #if successful
            return result
        else:
            flash("this email already exists")
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
    # if not 'logged_in' in session:
    if request.method == 'POST':
        #receiving data from html
        email = request.form.get('email')
        password = request.form.get('password')
        if check_acc(email, password): #if email and password are verified
            return redirect(url_for('cart', name=session['name'])) #redirect to cart and start a session
        else:
            flash("password or email is incorrect")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove all keys from the session dictionary
    session.clear()
    return redirect(url_for('login'))

@app.route('/cart', methods=['GET', 'POST'])

def cart():
    if 'logged_in' in session:
        conn = get_db_connection()
        usercart = conn.execute(f"SELECT u.product_ID, p.product_name, u.amount, p.price FROM '{session['ID']}_cart' AS u LEFT JOIN products AS p ON u.product_ID=p.product_ID").fetchall()
        #gets ALL items in user cart
        if request.method =='POST':
            quantities = {k: v for k, v in request.form.items() if k.startswith('quantity_')}
            if not quantities: 
                print('No quantity fields in form:', dict(request.form))
            for field_name, value in quantities.items():
                product_ID = field_name.split('_', 1)[1]
                try:
                    quantity = int(value)
                except ValueError:
                    continue
                conn.execute(
                    f"UPDATE '{session['ID']}_cart' SET amount=? WHERE product_ID=?",
                    (quantity, int(product_ID))
                )
            conn.commit()
            return redirect(url_for('cart'))

        return render_template('cart.html', name=session['name'],usercart=usercart)
    else: 
        return redirect(url_for('signup'))

@app.route('/checkout')
def checkout():
    conn = get_db_connection()
    order_data = conn.execute(f"SELECT product_ID, amount FROM '{session['ID']}_cart'").fetchall()
    #fetching all items from user cart
    for item in order_data:
        conn.execute("INSERT INTO orders (user_ID, product_ID, quantity) VALUES (?, ?, ?)", (session['ID'], item['product_ID'], item['amount']))
        conn.commit()
        #adds each item as an instance in the orders table
    conn.execute(f"DELETE FROM '{session['ID']}_cart'") #clears user table
    conn.commit()
    return redirect(url_for('cart'))

@app.route('/remove_product')
def remove_product():
    conn = get_db_connection()
    pID = request.args.get('pID')
    conn.execute(f"DELETE FROM '{session['ID']}_cart' WHERE product_ID = ?", (pID,))
    conn.commit()
    return redirect(url_for('cart'))

@app.route('/manifest.json')

def manifest():

    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')

def service_worker():

    return app.send_static_file('service-worker.js')

if __name__ == '__main__':

    app.run(debug=True)