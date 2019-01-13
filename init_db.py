#!env/bin/python3

from models import UserManager, EnfantManager
import sqlite3
import re


data_base = "db.sqlite3"


def init_db():

    """Initialise la BDD -les compétences des programmes, la table des élèves """

    # Connexion bdd 
    db = sqlite3.connect(data_base)
    conn = db.cursor()

    # Rendre disponible l'utilisation des clés étrangères -> pas d'insertion dans domaines!
    # conn.execute("PRAGMA foreign_keys = ON")

    # Création des tables
    conn.execute("CREATE TABLE IF NOT EXISTS domaines \
                (id INTEGER PRIMARY KEY NOT NULL, \
                nom TEXT NOT NULL, \
                UNIQUE (nom))")  # domaines
    conn.execute("CREATE TABLE IF NOT EXISTS competences \
                (id INTEGER PRIMARY KEY NOT NULL, \
                nom TEXT NOT NULL, \
                position INTEGER NOT NULL, \
                domaine INTEGER NOT NULL, \
                UNIQUE (nom), \
                FOREIGN KEY(domaine) REFERENCES domaines(id))")  # Absence d'erreur en cas de violation!
    conn.execute("CREATE TABLE IF NOT EXISTS observables \
                (id INTEGER PRIMARY KEY NOT NULL, \
                nom TEXT NOT NULL, \
                competence INTEGER NOT NULL, \
                image TEXT, \
                niveau INTEGER CHECK (niveau == 0 OR niveau == 1 OR niveau == 2), \
                position INTEGER NOT NULL, \
                UNIQUE (nom), \
                FOREIGN KEY(competence) REFERENCES competences(id))")
    conn.execute("CREATE TABLE IF NOT EXISTS enfants \
                (id INTEGER PRIMARY KEY NOT NULL, \
                nom TEXT NOT NULL, \
                prenom TEXT NOT NULL, \
                sexe TEXT CHECK (sexe == 'F' OR sexe == 'M'), \
                date INTEGER NOT NULL, \
                UNIQUE (nom, prenom, date))")
    conn.execute("CREATE TABLE IF NOT EXISTS commentaires \
                (id INTEGER PRIMARY KEY NOT NULL, \
                enfant_id INTEGER NOT NULL, \
                commentaire TEXT NOT NULL, \
                date INTEGER NOT NULL, \
                FOREIGN KEY(enfant_id) REFERENCES enfants(id))")
    conn.execute("CREATE TABLE IF NOT EXISTS users \
                (id INTEGER PRIMARY KEY NOT NULL, \
                nom TEXT NOT NULL, \
                prenom TEXT NOT NULL, \
                login TEXT NOT NULL, \
                password TEXT NOT NULL, \
                is_staff INTEGER NOT NULL CHECK (is_staff == 1 OR is_staff == 0) \
                UNIQUE (login))")
    conn.execute("CREATE TABLE IF NOT EXISTS observables_e \
                (id INTEGER PRIMARY KEY NOT NULL, \
                obs INTEGER NOT NULL, \
                enfant INTEGER NOT NULL, \
                image TEXT, \
                date INTEGER NOT NULL, \
                FOREIGN KEY(enfant) REFERENCES enfants(id)) \
                FOREIGN KEY(obs) REFERENCES observables(id))")
    
    # Photos dans rep global ou dans rep individuel -> hors BDD

    # Domaines et compétences ______________________________________________________
    # Récupération du fichier csv
    fichier = open("docs/competences", "r")
    lignes = fichier.readlines()
    fichier.close()

    # Traitement des données
    domaine_id = 0
    for ligne in lignes:
        if ligne[0] is '#':
            conn.execute("INSERT INTO domaines (nom) VALUES ('%s')" % (ligne[1:-1]))
            domaine_id += 1
        else:
            data = ligne.replace("\n", "").split('|')
            conn.execute("INSERT INTO competences (nom, domaine) \
                        VALUES ('%s', %d)" % (data[1], domaine_id))

    # Observables __________________________________________________________________
    # Récupération du fichier csv
    fichier = open("docs/observables", "r")
    lignes = fichier.readlines()
    fichier.close()

    # Traitement des données
    competence_id = 0
    for ligne in lignes:
        if re.match(r"^[\d]", ligne):
            competence_id += 1
        else:
            conn.execute("INSERT INTO observables (nom, competence) \
                          VALUES ('%s', %d)" % (ligne[:-1], competence_id))

    db.commit()
    db.close()


def update_observables():

    """Mettre à jour les observables à partir du fichier"""

    # Connexion bdd
    db = sqlite3.connect(data_base)
    conn = db.cursor()

    fichier = open("docs/observables", "r")
    lignes = fichier.readlines()
    fichier.close()

    # Traitement des données
    obs_id = 1
    for ligne in lignes:
        if re.match(r"^[\d]", ligne) is None:
            conn.execute("UPDATE observables \
                          SET nom = '%s' \
                          WHERE id = %d" % (ligne, obs_id))
            obs_id += 1

    db.commit()
    db.close()


def init_enfants():
    db = sqlite3.connect(data_base)
    conn = db.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS observables_e \
                (obs INTEGER NOT NULL, \
                enfant INTEGER NOT NULL, \
                image TEXT, \
                date INTEGER NOT NULL, \
                FOREIGN KEY(enfant) REFERENCES enfants(id), \
                FOREIGN KEY(obs) REFERENCES observables(id), \
                PRIMARY KEY (obs, enfant))")
    db.commit()
    conn.execute('SELECT id, nom, prenom, date, sexe FROM enfants ORDER BY date DESC')
    enfants = conn.fetchall()
    for enf in enfants:
        conn.execute("SELECT * FROM enfant_%s \
                      WHERE date is not null" % enf[0])
        obs = conn.fetchall()
        for o in obs:
            print(o)
            if o[1] is not None:
                conn.execute("INSERT INTO observables_e (obs, enfant, image, date) \
                              VALUES (%d, %d, '%s', %d)" % (o[0], enf[0], o[1], o[2]))
            else:
                conn.execute("INSERT INTO observables_e (obs, enfant, date) \
                              VALUES (%d, %d, %d)" % (o[0], enf[0], o[2]))
        conn.execute("DROP TABLE enfant_%s" % enf[0])
    db.commit()
                      


if __name__ == '__main__':
    init_db()
    UserManager(data_base).add_user('Silver', 'John', 'longjohn', 'pirate', 1)
