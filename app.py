from flask import Flask, request, redirect, url_for, render_template, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import aiml
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

DATABASE = 'users.db'
BRAIN_FILE = './model/brain.dump'
port = 5009

# Initialize AIML kernel
k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="./model/std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

def get_db():
    """Open a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database with the schema from schema.sql."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        national_id = request.form.get('national_id')
        gender = request.form.get('gender')
        email = request.form.get('email')
        account_type = request.form.get('account_type')

        print("get files is ok")

        # Validate required fields
        if not all([name, mobile, national_id, gender, email, account_type]):
            flash('All fields are required!')
            return redirect(url_for('register'))
        
        print("is ok")

        db = get_db()
        print("get db is ok")

        # Check if the national_id already exists
        existing_user = db.execute(
            'SELECT * FROM users WHERE national_id = ?',
            (national_id,)
        ).fetchone()

        if existing_user:
            flash('User with this National ID is already registered. Please log in.')
            return redirect(url_for('login'))


        try:
            db.execute(
                'INSERT INTO users (name, mobile, national_id, gender, email, account_type) VALUES (?, ?, ?, ?, ?, ?)',
                (name, mobile, national_id, gender, email, account_type)
            )
            db.commit()
            flash('Registration successful! Please log in.')

            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            db.rollback()
            flash('An error occurred while registering. Please try again.')
        except Exception as e:
            print(e)
            db.rollback()
            flash(f'Error inserting data into the database: {e}')

        return redirect(url_for('register'))

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("isssssss")
        national_id = request.form.get('national_id')

        if not national_id:
            print("oooo")
            flash('National ID is required!')
            return redirect(url_for('login'))

        db = get_db()
        user = db.execute(
            'SELECT name, national_id FROM users WHERE national_id = ?',
            (national_id,)
        ).fetchone()

        if user:
            session['national_id'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            print("npp")
            flash('Invalid National ID.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'national_id' in session:
        db = get_db()
        user = db.execute(
            'SELECT name, mobile, national_id, gender, email, account_type FROM users WHERE national_id = ?',
            (session['national_id'],)
        ).fetchone()

        if user:
            user_dict = {
                'name': user[0],
                'mobile': user[1],
                'national_id': user[2],
                'gender': user[3],
                'email': user[4],
                'account_type': user[5]
            }
            return render_template('dashboard.html', user=user_dict)
        else:
            flash('User not found.')
            return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['message']
        response = get_chatbot_response(user_input)
        return jsonify({'response': response})

    return render_template('chat.html')

def get_chatbot_response(user_input):
    """Get response from AIML chatbot."""
    respond = k.respond(user_input)
    respond = fix_respond(user_input, respond)
    print(type(user_input))
    return respond


def fix_respond(user_input : str, respond : str) -> str:
    if "login" in user_input.lower():
        message = f"for login go to this link => http://127.0.0.1:{port}/login"
        respond += ("\n" + message)

    if "register" in user_input.lower():
        message = f"for login go to this link => http://127.0.0.1:{port}/register"
        respond += ("\n" + message)
    
    if len(respond) == 0:
        respond = "Please only ask banking questions and avoid asking miscellaneous questions"
    
    return respond



if __name__ == '__main__':
    app.run(debug=True, port=port)





        
