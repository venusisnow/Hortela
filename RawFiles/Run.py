import datetime
try:
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

    cok = None
    def loadCok(email, passw, nome, tel=None, end=None, access=1):
        global cok

        cok = [email, passw, nome, tel, end, access]
        for i, k in enumerate(cok):
            if k == None:
                cok[i] = "Não Definido"
    def unloadCok():
        global cok
        cok = None

    # No url redirect
    @app.route('/')
    def empt():
        return flask.redirect('index')

    @app.route('/index')
    def index():
        return flask.render_template("index.html", u=cok)
    @app.route('/login')
    def login():
        return flask.render_template("login.html")
    @app.route('/sign')
    def sign():
        return flask.render_template("sign.html")
    @app.route('/profile')
    def profileH():
        if cok is None:
            return flask.redirect('/login')
        else:
            return flask.render_template('profile.html', u=cok)
    @app.route('/profile/logout')
    def logout():
        unloadCok()
        return flask.redirect("/login")
    @app.route('/redefinePass')
    def redPass():
        return flask.render_template("redefinir.html")

    # Form send
    @app.route('/profile/dltProf', methods=['POST'])
    def deleteProfile():
        if cok == None:
            return flask.redirect('/login')
        else:
            email = flask.request.form.get('emailD')
            passw = flask.request.form.get('passD')
            name = flask.request.form.get('nameD')

            if email == cok[0] and passw == cok[1] and name == cok[2]:

                with sqlite3.connect( configurationsInfoTXT['data'] ) as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM user WHERE email = ? AND pass = ? AND nome = ?", (email, passw, name))

                    return flask.redirect('/login')
            else:
                return flask.redirect('/profile?error=2')
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
                loadCok(email, passw, r[1], r[4], r[5], r[6])

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
    @app.route('/profile/send', methods=['POST'])
    def editProfile():
        Oemail = flask.request.form.get('Oemail')
        email = flask.request.form.get('email')
        end = flask.request.form.get('end')
        tel = flask.request.form.get('tel')
        nome = flask.request.form.get('name')

        if tel == "Não Definido":
            tel = None
        if end == "Não Definido":
            end = None

        # Recreate connection each time to prevent threading issues
        with sqlite3.connect(configurationsInfoTXT['data']) as conn:
            c = conn.cursor()

            loadCok(email, cok[1], nome, tel, end)

            if Oemail == email:
                c.execute("UPDATE user SET nome = ?, telefone = ?, endereco = ?"
                          "WHERE email = ?", (nome, tel, end, email))

                return flask.redirect("/profile")
            else:
                # Bypass the sql-injection
                c.execute("SELECT * FROM user WHERE email = ?", (email,))
                r = c.fetchone()

                if r == None:
                    c.execute("UPDATE user SET nome = ?, email = ?, telefone = ?, endereco = ?"
                              "WHERE email = ?", (nome, email, tel, end, Oemail))

                    return flask.redirect("/profile")

                else:
                    return flask.redirect(f"/profile?error=1")

    if __name__ == '__main__':
        ip = configurationsInfoTXT['ip']
        port = configurationsInfoTXT['port']
        app.run(host=ip, port=port, debug=True)
        os.system("pause")

except Exception as e:
    with open("log.txt", 'w') as f:
        f.write(f"[{datetime.datetime.now()}] {e}\n")