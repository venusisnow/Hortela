import click
import itsdangerous
import jinja2
import markupsafe
import werkzeug
import flask
import sqlite3
import os
import json


basePath = os.getcwd()
app = flask.Flask(__name__, template_folder=os.path.join(basePath, 'templates'), static_folder=os.path.join(basePath, 'static'))
configurationsInfoTXT = json.load(open("config.txt"))

cok = ['null', 'null']

# No url redirect
@app.route('/')
def empt():
    return flask.redirect('index.html')
@app.route('/index')
def index():
    return flask.render_template("index.html")
@app.route('/login')
def login():
    return flask.render_template("login.html")
@app.route('/sign')
def sign():
    return flask.render_template("sign.html")
@app.route('/profile')
def profileH():
    if cok[0] == 'null':
        return flask.redirect('/login')
    else:
        return flask.render_template('profile.html', u=cok)
@app.route('/redefinePass')
def redPass():
    return flask.render_template("redefinir.html")

# Form things
@app.route('/sign/send', methods=['POST'])
def registerF():
    # Register
    email = flask.request.form['email']
    passw = flask.request.form['password']
    nome = flask.request.form['nome']

    # Recreate connection each time to prevent threading issues
    with sqlite3.connect( configurationsInfoTXT['data'] ) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE email = ?", (email,))
        r = c.fetchone()

        if r == None:
            c.execute("INSERT INTO user (nome, email, pass, access) VALUES (?,?,?,?)", (nome, email, passw, 1))

            return flask.redirect("/login")
        else:
            return flask.redirect(f"/sign?error=1&n={nome}&p={passw}")
@app.route('/login/send', methods=['POST'])
def loginR():
    # Login
    email = flask.request.form.get('email')
    passw = flask.request.form.get('password')

    # Recreate connection each time to prevent threading issues
    with sqlite3.connect( configurationsInfoTXT['data'] ) as conn:
        c = conn.cursor()

        # Bypass the sql-injection
        c.execute("SELECT * FROM user WHERE email = ? AND pass = ?", (email, passw))
        r = c.fetchone()

        if r == None:
            return flask.redirect("/login?error=1")
        else:
            global cok

            cok = [email, passw]
            return flask.redirect('/profile')
@app.route('/redefinePass/send', methods=['POST'])
def redifPass():
    # Change Pass
    email = flask.request.form.get('email')
    passw = flask.request.form.get('password')
    Opassw = flask.request.form.get('oldPass')

    # Recreate connection each time to prevent threading issues
    with sqlite3.connect(configurationsInfoTXT['data']) as conn:
        c = conn.cursor()

        # Bypass the sql-injection
        c.execute("SELECT * FROM user WHERE email = ? AND pass = ?", (email, Opassw))
        r = c.fetchone()

        if r == None:
            return flask.redirect(f"/redefinePass?error=1")

        else:
            c.execute("UPDATE user SET pass = ? WHERE email = ? and pass = ?", (passw, email, Opassw))

            return flask.redirect("/login")

if __name__ == '__main__':
    ip = configurationsInfoTXT['ip']
    port = configurationsInfoTXT['port']
    app.run(host=ip, port=port, debug=True)
    os.system("pause")