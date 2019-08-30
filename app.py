"""TP Python - Rock bands website"""
import os
import sqlite3
from flask import (Flask, render_template, redirect, url_for, request)

APP = Flask(__name__)

# Create DB if doesn't exist
if not os.path.exists('database.db'):
    DB = sqlite3.connect('database.db')
    # Read schema.sql
    with open('schema.sql') as F:
        DB.cursor().executescript(F.read())


def get_db():
    """Return DB connexion"""
    return sqlite3.connect('database.db')


# Accueil
@APP.route('/', methods=['GET'])
@APP.route('/accueil', methods=['GET'])
def accueil():
    """Displays accueil"""
    return render_template('accueil.html')


# Groupes
@APP.route('/groupes', methods=['GET'])
def groupes():
    """Displays all groupes in DB"""
    req_groupe = 'SELECT id, nom, description FROM groupe'
    req_commentaire = 'SELECT auteur, commentaire, groupe FROM commentaire ORDER BY creation'
    search = request.args.get('search')

    # If there is a filter
    if search is not None:
        req_groupe += " WHERE nom LIKE '%{}%'".format(search)

    req_groupe += ' ORDER BY nom'
    
    results_groupe = list(get_db().cursor().execute(req_groupe))
    results_commentaire = list(get_db().cursor().execute(req_commentaire))

    return render_template('groupes.html', search=search,
                           groupes=results_groupe, commentaires=results_commentaire)


# Ajout groupe
@APP.route('/ajoutgroupe', methods=('GET', 'POST'))
def ajout_groupe():
    """If GET: displays form, else if POST: tries to insert in DB"""
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        error = None
        database = get_db()

        # If name is empty, cancels
        if not nom:
            error = 'Le nom du groupe doit etre renseigne.'
        # If description is empty, cancels
        if not description:
            if error is not None:
                error += '\nLa description du groupe doit etre renseignee.'
            elif error is None:
                error = 'La description du groupe doit etre renseignee.'

        # If groupe already exists, cancels
        if database.execute('SELECT id FROM groupe WHERE nom = ?',
                            (nom, )).fetchone() is not None:
            error = 'Le groupe {} est deja enregistre.'.format(nom)

        # If there is no error insert group in DB and redirect to groupes page
        if error is None:
            database.execute('INSERT INTO groupe(nom, description) VALUES(?, ?)',
                             (nom, description, ))
            database.commit()
            return redirect(url_for('groupes'))

        # If there is an error, displays form with error
        return render_template('ajoutgroupe.html', error=error)

    return render_template('ajoutgroupe.html')


# Ajout groupe
@APP.route('/ajoutcommentaire', methods=['POST'])
def ajout_commentaire():
    """Insert commentaire in DB"""
    auteur = request.form['auteur']
    commentaire = request.form['commentaire']
    groupe = request.form['groupe']
    error = None
    database = get_db()

    # If auteur is empty
    if not auteur:
        auteur = 'Anonyme'

    # If commentaire is empty
    if not commentaire:
        error = 'Le commentaire ne peut pas etre vide.'

    if error is None:
        database.execute('INSERT INTO commentaire(groupe, auteur, commentaire) VALUES(?, ?, ?)',
                         (groupe, auteur, commentaire))
        database.commit()

    return redirect(url_for('groupes'))


if __name__ == "__main__":
    APP.run(debug=True)
