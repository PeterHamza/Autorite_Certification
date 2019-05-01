from flask import Flask, request, render_template, flash, g, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = "Epsi_c_est_cool"
app.config['MONGO_DB'] = "CA"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CA'

mongo = PyMongo(app)

@app.route('/', methods=["GET"])
def index():
    if getattr(g, 'user', None) is None:
        return render_template("auth/login.html")
    return render_template('auth/index.html')

@app.route("/connexion/", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        user = mongo.db.user

        if user.count( {"login": request.form["identifiant"], "password": request.form["password"] } ) != 0:
            g.user = request.form["identifiant"]
            return render_template("auth/index.html")
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
    return render_template('auth/register.html')

@app.route("/", methods=["POST"])
def upload():
    fichier = request.files["certificat"]
    if fichier:
        mon_fichier = fichier.filename
        # if mon_fichier.rsplit('.', 1)[1] == 'csr':
        #     file = mongo.db.file
        #     file.insert({"file": request.files['certificat']})
    return render_template("auth/index.html")

if __name__ == '__main__':
    app.run(port="8080", debug=True)
