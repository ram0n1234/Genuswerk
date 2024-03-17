from flask import render_template, redirect, url_for, session, jsonify
from app import app, db
from app.forms import LoginForm, RegistrierungsForm, KommentarForm, RezeptForm
from hashlib import sha256
from app.models import Benutzer, Rezepte, Kommentare

# Route für Hauptseite bzw. Loginseite
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if "BenutzerID" in session:
        rezepte = Rezepte.query.all()
        return render_template('index.html', rezepte=rezepte)
    else:
        form = LoginForm()
        # prüfen ob Anmeldemaske ausgefüllt wurde
        if form.validate_on_submit():
            sql = Benutzer.query.filter_by(benutzername=form.Benutzername.data, passwort=sha256(form.Passwort.data.encode('utf-8')).hexdigest()).first()
            if sql is None:
                return render_template('login.html', form=form)
            else:
                # Session-Variable erstellen und ID des Benutzers als Inhalt abspeichern
                session["BenutzerID"] = sql.id
                return redirect(url_for('index'))
        # Es existiert keine Benutzer-Session -> Anmeldemaske anzeigen
        else:
            return render_template('login.html', form=form)

# Route für Registrierung
@app.route('/registrierung', methods=['GET','POST'])
def registrierung():
    form = RegistrierungsForm()
    # Prüfen ob Registrierungs-Formular ausgefüllt wurde
    if form.validate_on_submit():
        # Pruefen ob es bereits einen entsprechenden Benutzername gibt
        sql = Benutzer.query.filter_by(benutzername=form.Benutzername.data).first()
        if sql is None:
            # Quelle - Type Error onhe Encode
            # URL: https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing
            sql = Benutzer(benutzername=form.Benutzername.data,email=form.EMail.data,passwort=sha256(form.Passwort.data.encode('utf-8')).hexdigest())
            db.session.add(sql)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('registrierung'))
    # Ansonsten Registrierungs-Formular anzeigen     
    else:
        return render_template('registrierung.html', form=form)

# Route für Logout
@app.route('/logout')
def logout():
    # Prüfen ob Benutzer authentifiziert ist
    if "BenutzerID" in session:
        # Session-Variable löschen und zu Index weiterleiten
        session.pop("BenutzerID", None)
        return redirect(url_for('index'))

# Route für Rezepterfassung
@app.route('/rezept_erfassen', methods=['GET','POST'])
def rezept_erfassen():
    form = RezeptForm()
    # Prüfen ob Benutzer authentifiziert ist
    if "BenutzerID" in session:
        # Wenn Rezept übermittelt wird, Rezept in DB speichern
        if form.validate_on_submit():
            sql = Rezepte(titel=form.Titel.data,beschreibung=form.Beschreibung.data,zutaten=form.Zutaten.data,kochanleitung=form.Kochanleitung.data,zubereitungsdauer=form.Zubereitungsdauer.data,fk_benutzer_id=session["BenutzerID"])
            db.session.add(sql)
            db.session.commit()
            # Weiterleiten zu Index bzw. Übersicht
            return redirect(url_for('index'))
        # Ansonsten Rezept erfassen Formular anzeigen
        else:
            return render_template('rezept_erfassen.html', form=form)
    # Falls Benutzer nicht authentifiziert, weiterleiten zu Index
    else:
        return redirect(url_for('index'))

# Route für Rezept-Detailansicht
@app.route('/rezept/<id>', methods=['GET','POST'])
def rezept(id):
    form = KommentarForm()
    # Prüfen ob Benutzer authentifiziert ist
    if "BenutzerID" in session:
        # Wenn Kommentar übermittelt wird, Kommentar in DB speichern
        if form.validate_on_submit():
            sql = Kommentare(kommentar=form.Kommentar.data, fk_benutzer_id=session["BenutzerID"], fk_rezept_id=id)
            db.session.add(sql)
            db.session.commit()
            return redirect(url_for('rezept', id=id))
        # Ansonsten Seite ausgeben
        else:
            rezept = Rezepte.query.filter_by(id = id).first()
            kommentare = db.session.query(Kommentare, Benutzer.benutzername).join(Benutzer, Kommentare.fk_benutzer_id == Benutzer.id).all()
            return render_template('rezept.html', rezept=rezept, form=form, kommentare=kommentare)
    # Falls Benutzer nicht authentifiziert, weiterleiten zu Index
    else:
        return redirect(url_for('index'))    

# Routen für API
@app.route('/api/get_allUsers')
def api_get_allUsers():
    sql = Benutzer.query.all()
    return jsonify([s.toDict() for s in sql])

@app.route('/api/get_RezeptByUserID/<id>')
def api_get_KommentarByUserID(id):
    sql = Rezepte.query.filter_by(fk_benutzer_id = id)
    return jsonify([s.toDict() for s in sql])