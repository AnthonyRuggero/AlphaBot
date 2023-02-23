from flask import Flask, render_template, redirect, url_for, request
import time
import AlphaBot
import sqlite3
import random
import string
import hashlib

app = Flask(__name__)

def validate(username, password):
    completion = False
    con = sqlite3.connect('./movimentiAB.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[1]
        dbPass = row[2]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    psw = user_password.encode()
    password_login = hashlib.md5(psw).hexdigest()
    return hashed_password == password_login

def generate_random_string(string_length=30):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))
#print(generate_random_string())

secretString = generate_random_string()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Credenziali non corrette. Riprova!'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)


@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('./movimentiAB.db')
        cur = con.cursor()
        cur.execute("INSERT INTO Users VALUES({username}, {password})")
        return redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route(f'/{secretString}', methods=['GET', 'POST'])
def secret():
    robot = AlphaBot.AlphaBot()
    if request.method == 'POST':
        if request.form.get('avanti') == 'avanti':
            print("avanti")
            robot.forward()
            time.sleep(0.5)

        elif  request.form.get('indietro') == 'indietro':
            print("indietro")
            robot.backward()
            time.sleep(0.5)
        
        elif request.form.get('destra') == 'destra':
            print("destra")
            robot.right()
            time.sleep(0.3)
            
        elif request.form.get('sinistra') == 'sinistra':
            print("sinistra")
            robot.left()
            time.sleep(0.3)
        
        elif request.form.get('stop') == 'stop':
            print("stop")
            robot.stop()

        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)