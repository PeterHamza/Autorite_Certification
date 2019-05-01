from flask import Flask, request, render_template, flash
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = "Epsi_c_est_cool"
app.config['MONGO_DB'] = "CA"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CA'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.route("/connexion/", methods=["GET", "POST"])
def connexion():
    if request.method == "GET":
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/inscription/', methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        user = mongo.db.user

        if request.form["password"] != request.form["password_confirmation"]:
            flash(u"Les mots de passes ne sont pas identiques", "error_password")
        elif user.count( {"login" : request.form["identifiant"]} ) != 0:
            flash(u"L'utilisateur existe déjà", "error_user")
        else:
            login = request.form["identifiant"]
            password = request.form["password"]
            user.insert({
            "login": login, "password": password
            })
            flash(u"Vous êtes inscrit", "inscription")
    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(host=192.168.33.250, debug=True)
