from datetime import datetime
from app import db

class Benutzer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), nullable=False)
    passwort = db.Column(db.String(64), nullable=False)

    def toDict(self):
        return dict(id=self.id, benutzername=self.benutzername, email=self.email)

class Rezepte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(60), nullable=False)
    beschreibung = db.Column(db.String(600), nullable=False)
    zutaten = db.Column(db.String(600), nullable=False)
    kochanleitung = db.Column(db.String(600), nullable=False)
    zubereitungsdauer = db.Column(db.Integer, nullable=False)
    datum_erstellung = db.Column(db.DateTime, default=datetime.utcnow)
    fk_benutzer_id = db.Column(db.Integer, db.ForeignKey(Benutzer.id))

    def toDict(self):
        return dict(id=self.id, titel=self.titel, beschreibung=self.beschreibung, zutaten=self.zutaten, zubereitungsdauer=self.zubereitungsdauer, kochanleitung=self.kochanleitung)

class Kommentare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kommentar = db.Column(db.String(600), nullable=False)
    datum_erstellung = db.Column(db.DateTime, default=datetime.utcnow)
    fk_benutzer_id = db.Column(db.Integer, db.ForeignKey(Benutzer.id))
    fk_rezept_id = db.Column(db.Integer, db.ForeignKey(Rezepte.id))
