import psycopg2
from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="7326",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                       (str(username), str(password)))
        records = list(cursor.fetchall())

        if username == '' or password == '':
            message = "Введите логин или пароль"
            return render_template('login.html', message=message)

        if not records:
            message = f"Пользователя {username} не существует"
            return render_template('login.html', message=message)


        data = {
            "full_name": records[0][1],
            "password": records[0][3],
            "username": records[0][2],
        }
        return render_template('account.html', data=data)
    return render_template('login.html')


@app.route('/reg/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if name == '' or login == '' or password == '':
            message = "Вы не ввели все данные"
            return render_template('registration.html', message=message)

        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())

        if records:
            message = f"Пользователь с логином {login} уже есть в системе"
            return render_template('registration.html', message=message)

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')
    return render_template('registration.html')
