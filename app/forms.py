from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    Benutzername = StringField('Benutzername', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    Passwort = PasswordField('Passwort:', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    submit = SubmitField('Anmelden')

class RegistrierungsForm(FlaskForm):
    Benutzername = StringField('Benutzername', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    EMail = StringField('E-Mail', validators=[DataRequired(message="Pflichtfeld, bitte angeben!"), Email(message="Bitte gültige E-Mailadresse angeben!")])
    Passwort = PasswordField('Passwort', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    submit = SubmitField('Registrieren')

class RezeptForm(FlaskForm):
    Titel = StringField('Titel', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    Beschreibung = TextAreaField('Beschreibung', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    Zutaten = TextAreaField('Zutaten', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    Kochanleitung = TextAreaField('Kochanleitung', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    Zubereitungsdauer = IntegerField('Zubereitungsdauer (in Minuten)', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    submit = SubmitField('Speichern')

class KommentarForm(FlaskForm):
    Kommentar = StringField('Kommentar', validators=[DataRequired(message="Pflichtfeld, bitte angeben!")])
    submit = SubmitField('Speichern')