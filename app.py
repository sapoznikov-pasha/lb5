import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db", user="postgres", password="75547554a", host="localhost", port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                return render_template('login.html', error='Login failed! Check username and password, then try again')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            try:
                return render_template('account.html', full_name=records[0][1], username=username, password=password)
            except IndexError:
                return render_template('login.html', error='Login failed! Check username and password, then try again')
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if not login or not password or not name:
            return render_template('registration.html',
                                   error='Registration failed! Check name, login and password, then try again')
        cursor.execute('SELECT 1 FROM service.users WHERE login=%s LIMIT 1', (str(login),))
        if cursor.fetchone():
            return render_template('registration.html', error="User with given username already exists")
        cursor.execute('INSERT INTO service.users(full_name, login, password) VALUES(%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')
