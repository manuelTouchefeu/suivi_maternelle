import sqlite3
from datetime import datetime
from bottle import request
import hashlib
import re
import glob
import os
from PIL import Image

# TODO: normaliser les insertions de texte dans la base: supprimer ', ", ....

data_base = 'db.sqlite3'


class Connection:
    def __init__(self):
        global data_base
        self.db = sqlite3.connect(data_base)
        self.conn = self.db.cursor()


class Domaine:
    def __init__(self, id_dom, nom, competences=None):
        self.id = id_dom
        self.nom = nom
        self.competences = competences if competences else {}


class Competence:
    def __init__(self, id_dom, id_comp, nom_comp, position=None, observables=None):
        self.domaine = id_dom
        self.id = id_comp
        self.nom = nom_comp
        self.position = position
        self.observables = observables if observables else {}


class Observable:
    def __init__(self, id_comp, id_obs, nom_obs, niveau=0, image=None, position=None):
        self.competence = id_comp
        self.id = id_obs
        self.nom = nom_obs
        self.image = image
        self.niveau = niveau  # 0 -> 2-4; 1 -> 4-5; 2 -> 5-6
        self.position = position


class ObsEnfant(Observable):
    def __init__(self, id_comp, id_obs, nom_obs, age, niveau=0, image=None, position=None, image_perso=None, date=None):
        Observable.__init__(self, id_comp, id_obs, nom_obs, niveau, image, position)
        self.image_perso = image_perso
        self.statut = 0
        self._date = self.set_date(date, age)

    def _get_date(self):
        if self._date is None:
            return None
        else:
            date = datetime.fromtimestamp(self._date)
            return "%d/%d/%d" % (date.day, date.month, date.year)
    date = property(_get_date)

    def set_date(self, date, age):
        self._date = date
        if date:
            self.statut = 0
        elif age > self.niveau:
            self.statut = 1
        elif age == self.niveau:
            self.statut = 2
        elif self.niveau > age:
            self.statut = 3
        return date

    def _get_statut(self):
        return {0: 'ok', 1: 'alerte', 2: 'suite', 3: 'passe'}[self.statut]
    statut2 = property(_get_statut)


class Commentaire:
    def __init__(self, id_com, enfant_id, texte=None, date=None):
        self.id_com = id_com
        self.enfant_id = enfant_id
        self.texte = texte
        self._date = date

    def _get_date(self):
        if self._date is None:
            return None
        else:
            date = datetime.fromtimestamp(self._date)
            return "%d/%d/%d" % (date.day, date.month, date.year)
    date = property(_get_date)

# class CommentaireManager
    

class DomaineManager(Connection):
    def __init__(self):
        Connection.__init__(self)

    def get_domaines(self):
        """ Récupérer l'id et le nom des domaines """
        self.conn.execute('SELECT id, nom FROM domaines')
        result = []
        for elt in self.conn.fetchall():
            result.append(Domaine(elt[0], elt[1]))
        return result

    def get_observable(self, id_obs):
        # id_comp, id_obs, nom_obs, niveau=0, image=None, position=None
        self.conn.execute("SELECT competence, id, nom, niveau, image, position \
                           FROM observables \
                           WHERE observables.id = %d" % id_obs)
        obs = self.conn.fetchone()
        return Observable(obs[0], obs[1], obs[2], obs[3], obs[4], obs[5])

    def get_competence(self, id_comp):
        self.conn.execute("SELECT competences.domaine, competences.id, competences.nom, competences.position, \
                           observables.id, observables.nom, observables.niveau, \
                           observables.image, observables.position \
                           FROM competences \
                           LEFT JOIN observables \
                           ON observables.competence = competences.id \
                           WHERE competences.id = %s" % id_comp)
        req = self.conn.fetchall()
        competence = Competence(req[0][0], req[0][1], req[0][2], req[0][3])
        for obs in req:
            if obs[4]:
                competence.observables[obs[8]] = Observable(obs[1], obs[4], obs[5], obs[6], obs[7], obs[8])
        return competence

    def get_observables_dom(self, id_dom):
        self.conn.execute("SELECT domaines.id, domaines.nom, \
                           competences.id, competences.nom, competences.position, \
                           observables.id, observables.nom, observables.niveau, \
                           observables.image, observables.position \
                           FROM competences \
                           LEFT JOIN observables \
                           ON observables.competence = competences.id \
                           INNER JOIN domaines \
                           ON competences.domaine = domaines.id \
                           WHERE domaines.id = %s" % id_dom)
        req = self.conn.fetchall()
        if req is []:
            self.conn.execute("SELECT nom FROM domaines WHERE id = %s" % id_dom)
            return Domaine(id_dom, self.conn.fetchone()[0])
        domaine = Domaine(req[0][0], req[0][1])
        for obs in req:
            # cle = obs[2] pour lancer set_position_comp()
            if obs[4] not in domaine.competences.keys():
                competence = Competence(domaine.id, obs[2], obs[3], obs[4])  # idem
                domaine.competences[obs[4]] = competence
            if obs[5]:
                domaine.competences[obs[4]].observables[obs[9]] = \
                    Observable(obs[2], obs[5], obs[6], obs[7], obs[8], obs[9])
        return domaine

    def set_position_comp(self, id_dom):
        """Pour initialiser la position des compétences."""
        domaine = self.get_observables_dom(id_dom)
        pos = 1
        for index in sorted(domaine.competences.keys()):
            competence = domaine.competences[index]
            self.conn.execute("UPDATE competences SET position = ? \
                               WHERE id = ?", (pos, competence.id))
            self.db.commit()
            pos += 1

    def set_position(self, id_dom):
        """ Pour initialiser la position des observables."""
        domaine = self.get_observables_dom(id_dom)
        for comp in domaine.competences.values():
            pos = 1
            for index in sorted(comp.observables.keys()):
                obs = comp.observables[index]
                self.conn.execute("UPDATE observables SET position = ? \
                                   WHERE id = ?", (pos, obs.id))
                self.db.commit()
                pos += 1

    def update_position(self, up, down):
        up = self.get_observable(up)
        down = self.get_observable(down)
        self.conn.execute("UPDATE observables SET position = ? \
                           WHERE id = ?", (up.position-1, up.id))
        self.conn.execute("UPDATE observables SET position = ? \
                           WHERE id = ?", (down.position+1, down.id))
        self.db.commit()
        up = self.get_observable(up.id)
        down = self.get_observable(down.id)
        return {'up': up, 'down': down}

    def update_position_comp(self, up, down):
        up = self.get_competence(up)
        down = self.get_competence(down)
        self.conn.execute("UPDATE competences SET position = ? \
                           WHERE id = ?", (up.position-1, up.id))
        self.conn.execute("UPDATE competences SET position = ? \
                           WHERE id = ?", (down.position+1, down.id))
        self.db.commit()
        up = self.get_competence(up.id)
        down = self.get_competence(down.id)
        return {'up': up, 'down': down}

    def update_text(self, id_item, text, genre):
        """Pour modifier le texte d'un observable ou d'une compétence."""
        if genre == 'observable':
            try:
                self.conn.execute("UPDATE observables SET nom = ? \
                                   WHERE id = ?", (text, id_item))
                self.db.commit()
                return True
            except sqlite3.IntegrityError:
                return False
        elif genre == 'competence':
            try:
                self.conn.execute("UPDATE competences SET nom = ? \
                                   WHERE id = ?", (text, id_item))
                self.db.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def add_obs(self, competence, nom, niveau=0):
        self.conn.execute("SELECT MAX(position) \
                           FROM observables \
                           WHERE competence = %d" % competence)
        a = self.conn.fetchone()
        if a[0]:
            position = a[0] + 1
        else:
            position = 1
        self.conn.execute("INSERT INTO observables (competence, nom, niveau, position) \
                           VALUES (?, ?, ?, ?)", (competence, nom, niveau, position))
        id_obs = self.conn.lastrowid
        self.db.commit()
        return self.get_observable(id_obs)

    def del_obs(self, id_observable):
        observable = self.get_observable(id_observable)
        competence = self.get_competence(observable.competence)
        self.conn.execute("DELETE \
                           FROM observables \
                           WHERE id = %d" % observable.id)
        modif = []
        for obs in competence.observables.values():
            if obs.position > observable.position:
                obs.position -= 1
                self.conn.execute("UPDATE observables \
                                   SET position = %d \
                                   WHERE id = %d" % (obs.position, obs.id))
                modif.append(obs)
        self.conn.execute("DELETE \
                           FROM observables_e \
                           WHERE obs = %d" % observable.id)
        path = "%s/static/images/" % os.getcwd()
        for enfant in EnfantManager(data_base).get_enfants():
            for f in os.listdir(path):
                if re.search("enfant_%s_%s\." % (enfant.id, id_observable), f):
                    os.remove(os.path.join(path, f))
                    break
        for f in os.listdir(path):
            if re.search("obs_%s\." % id_observable, f):
                os.remove(os.path.join(path, f))
                break

        self.db.commit()
        return modif

    def del_comp(self, id_comp):
        competence = self.get_competence(id_comp)
        domaine = self.get_observables_dom(competence.domaine)
        for obs in competence.observables.values():
            self.del_obs(obs.id)
        self.conn.execute("DELETE \
                           FROM competences \
                           WHERE id = %d" % id_comp)
        modif = []
        for comp in domaine.competences.values():
            if comp.position > competence.position:
                comp.position -= 1
                self.conn.execute("UPDATE competences \
                                   SET position = %d \
                                   WHERE id = %d" % (comp.position, comp.id))
                modif.append(comp)
        self.db.commit()
        return modif

    def add_image_obs(self, id_observable, filename):
        """ Pour ajouter une photo à un observable """
        self.conn.execute("UPDATE observables SET image = ? \
                           WHERE id = ?", (filename, id_observable))

        self.db.commit()

    def supp_image(self, obs_id):
        self.conn.execute("UPDATE observables \
                           SET image = NULL \
                           WHERE id = %s" % obs_id)
        path = "%s/static/images/" % os.getcwd()
        for f in os.listdir(path):
            if re.search("obs_%s\." % obs_id, f):
                os.remove(os.path.join(path, f))
                break
        self.db.commit()

    def niveau_observable(self, id_observable, niveau):
        self.conn.execute("UPDATE observables SET niveau = ? \
                           WHERE id = ?", (niveau, id_observable))
        self.db.commit()

    def add_comp(self, id_dom, text):
        self.conn.execute("SELECT MAX(position) \
                           FROM competences \
                           WHERE domaine = %d" % id_dom)
        position = self.conn.fetchone()[0]
        if position is None:
            position = 1
        else:
            position += 1
        self.conn.execute("INSERT INTO competences (domaine, nom, position) \
                           VALUES (?, ?, ?)", (id_dom, text, position))
        id_comp = self.conn.lastrowid
        self.db.commit()
        return self.get_competence(id_comp)


class Enfant:
    def __init__(self, id_enfant, nom, prenom, date, sexe, obs=None, com=None):
        age = (datetime.today().timestamp() - date) / 31536000
        if age > 5:
            age = 2
        elif age > 4:
            age = 1
        else:
            age = 0
        self.id = id_enfant
        self.nom = nom
        self.prenom = prenom
        self._date = date  # timestamp
        self.annee = int(self.date.split('/')[2])
        self.age = age
        self.sexe = sexe
        self.observables = obs
        self.commentaires = com

    def __repr__(self):
        return "{} {}".format(self.nom, self.prenom)

    def _get_date(self):
        date = datetime.fromtimestamp(self._date)
        return "%d/%d/%d" % (date.day, date.month, date.year)
    date = property(_get_date)


class EnfantManager(Connection):
    def __init__(self):
        Connection.__init__(self)

    def get_enfants(self):
        result = []
        self.conn.execute('SELECT id, nom, prenom, date, sexe FROM enfants ORDER BY date DESC')
        for elt in self.conn.fetchall():
            result.append(Enfant(elt[0], elt[1], elt[2], elt[3], elt[4]))
        return result

    def get_classe(self, annee, id_dom):
        """Récupérer tous les enfants d'une classe d'âge, et leurs observables pour un domaine donné."""
        enfants = [enfant for enfant in self.get_enfants() if enfant.annee == int(annee)]
        liste = []
        for enfant in enfants:
            liste.append(self.get_enfant(enfant.id, id_dom))
        return liste

    def get_domaine_enfant(self, enfant, id_dom):
        domaine = DomaineManager().get_observables_dom(id_dom)
        self.conn.execute("SELECT observables_e.image, observables_e.date, \
                                  observables.position, competences.position \
                           FROM observables_e \
                           INNER JOIN observables \
                           ON observables_e.obs = observables.id \
                           INNER JOIN competences \
                           ON observables.competence = competences.id \
                           INNER JOIN domaines \
                           ON competences.domaine = domaines.id \
                           WHERE domaines.id LIKE '%s' \
                           AND observables_e.enfant = %d" % (id_dom, enfant.id))
        # On doit pouvoir faire mieux pour caster les Observables en ObsEnfant !
        for index_comp, comp in domaine.competences.items():
            for index_obs, obs in comp.observables.items():
                domaine.competences[index_comp].observables[index_obs] = \
                    ObsEnfant(obs.competence, obs.id, obs.nom, enfant.age, obs.niveau, obs.image, obs.position)
        for obs in self.conn.fetchall():
            domaine.competences[obs[3]].observables[obs[2]].image_perso = obs[0]
            domaine.competences[obs[3]].observables[obs[2]].set_date(obs[1], enfant.age)
        return domaine

    def get_enfant(self, id_enfant, id_dom=None):
        self.conn.execute("SELECT id, nom, prenom, date, sexe \
                           FROM enfants \
                           WHERE id = %d" % id_enfant)
        enf = self.conn.fetchone()
        enfant = Enfant(enf[0], enf[1], enf[2], enf[3], enf[4])

        # Ajouter les observables (un domaine)
        if id_dom:
            enfant.observables = self.get_domaine_enfant(enfant, id_dom)

        # Ajouter les commentaires (id - enfant_id - commentaire - date)
        self.conn.execute("SELECT * \
                           FROM commentaires \
                           WHERE enfant_id = %d" % enfant.id)
        enfant.commentaires = [Commentaire(commentaire[0], commentaire[1], commentaire[2], commentaire[3])
                               for commentaire in self.conn.fetchall()]

        return enfant 

    def add_enfant(self, nom, prenom, sexe, date):
        self.conn.execute("INSERT INTO enfants (nom, prenom, sexe, date) \
                           VALUES (?, ?, ?, ?)", (nom, prenom, sexe, date))
        self.db.commit()

    def update_enfant_image(self, enfant_id, obs_id, image):
        if self.conn.execute("SELECT enfant, obs \
                              FROM observables_e \
                              WHERE obs = %d \
                              AND enfant = %d" % (obs_id, enfant_id)).fetchone() is None:
            self.valide(enfant_id, obs_id, datetime.today().timestamp())
        self.conn.execute("UPDATE observables_e \
                           SET image = '%s' \
                           WHERE obs = %d \
                           AND enfant = %d" % (image, obs_id, enfant_id))
        self.db.commit()

    def supp_enfant_image(self, enfant_id, obs_id):
        self.conn.execute("UPDATE observables_e \
                           SET image = NULL \
                           WHERE obs = ? \
                           AND enfant = ?", (obs_id, enfant_id))
        path = "%s/static/images/" % os.getcwd()
        for f in os.listdir(path):
            if re.search("enfant_%s_%s\." % (enfant_id, obs_id), f):
                os.remove(os.path.join(path, f))
                break
        self.db.commit()

    def valide(self, id_e, id_o, date):
        """ Valide un observable """
        self.conn.execute("INSERT INTO observables_e (obs, enfant, date)\
                           VALUES (%d, %d, %d)" % (id_o, id_e, date))
        self.db.commit()

    def annule_obs_enfant(self, id_o, id_e):
        self.conn.execute("DELETE FROM observables_e \
                           WHERE obs = %d \
                           AND enfant = %d" % (id_o, id_e))
        self.db.commit()

    def add_commentaire(self, id_enfant, texte, date):
        self.conn.execute("INSERT INTO commentaires (enfant_id, commentaire, date) \
                           VALUES ('%s', '%s', %d)" % (id_enfant, texte, date))
        self.db.commit()

    def supp_commentaire(self, id_com):
        self.conn.execute("DELETE FROM commentaires \
                           WHERE id = %s" % id_com)
        self.db.commit()

    def update_commentaire(self, id_com, texte):
        self.conn.execute("UPDATE commentaires \
                           SET commentaire = '%s' \
                           WHERE id = %s" % (texte, id_com))
        self.db.commit()

    def supp_enfant(self, id_enfant):
        self.conn.execute("DELETE FROM enfants \
                           WHERE id=%d" % id_enfant)
        self.conn.execute("DELETE FROM observables_e \
                           WHERE enfant=%d" % id_enfant)
        self.conn.execute("DELETE FROM commentaires \
                           WHERE enfant_id=%d" % id_enfant)
        self.db.commit()
        for file in glob.glob('static/images/enfant_%d_*' % id_enfant):
            os.remove(file)
        return id_enfant


class User:
    def __init__(self, user_id, nom, prenom, login, is_staff):
        self.id = user_id
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.is_staff = is_staff  # 0 ou 1 (Sqlite ne gère pas les booléens)

    def __repr__(self):
        return "{} {}".format(self.prenom, self.nom)

    def _get_statut(self):
        statuts = {0: 'Utilisateur', 1: 'Administrateur'}
        return statuts[self.is_staff]
    statut = property(_get_statut)


class UserManager(Connection):
    def __init__(self):
        Connection.__init__(self)

    def add_user(self, nom, prenom, login, password, is_staff):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn.execute("INSERT INTO users (nom, prenom, login, password, is_staff) \
                           VALUES ('%s', '%s', '%s', '%s', %d)" % (nom, prenom, login, password, is_staff))
        self.db.commit()

    def supp_user(self, user_id):
        self.conn.execute('DELETE FROM users \
                           WHERE id=%d' % user_id)
        self.db.commit()

    def authentication(self, login, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        self.conn.execute("SELECT id, nom, prenom, login, is_staff \
                           FROM users \
                           WHERE login=? AND password=?", (login, password))
        res = self.conn.fetchone()
        if res is None:
            return None
        return User(res[0], res[1], res[2], res[3], res[4])

    def get_user(self, user_id):
        self.conn.execute("SELECT id, nom, prenom, login, is_staff \
                           FROM users \
                           WHERE id=%d" % user_id)
        res = self.conn.fetchone()
        if res:
            return User(res[0], res[1], res[2], res[3], res[4])
        return None

    def get_users(self):
        self.conn.execute("SELECT id, nom, prenom, login, is_staff \
                           FROM users")
        users = []
        for user in self.conn.fetchall():
            users.append(User(user[0], user[1], user[2], user[3], user[4]))
        return users

    def is_user_test(self):
        cookie = request.get_cookie("user", secret='some-secret-key')
        if cookie:
            return self.get_user(int(cookie))
        return None

    def is_staff_test(self):
        user = self.is_user_test()
        if user and user.is_staff == 1:
            return user
        return None

    def toggle_statut(self, user_id):
        user = self.get_user(user_id)
        user.is_staff = 1 if user.is_staff == 0 else 0
        self.conn.execute("UPDATE users \
                           SET is_staff=%d \
                           WHERE id=%d" % (user.is_staff, user_id))
        self.db.commit()
        return user


def personnalise(obs, nom, sexe):
    obs = re.sub(r"[Ll]’enfant", nom, obs)
    if sexe == 'F':
        obs = re.sub(r"([iI]l)·([eE]lle)", r"\2", obs)
        obs = re.sub(r"([A-Za-zé]+)·(e)", r"\1"+r"\2", obs)
    else:
        obs = re.sub(r"([iI]l)·([eE]lle)", r"\1", obs)
        obs = re.sub(r"([A-Za-zé]+)·e", r"\1", obs)
    return obs


def process_image(file, obs_id, enfant=None):
    ext = os.path.splitext(file.filename)[1]
    if ext not in ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'):
        return None
    image = Image.open(file.file)
    if enfant is None:
        name = 'obs_%s%s' % (obs_id, ext)
    else:
        name = "enfant_%s_%s%s" % (enfant, obs_id, ext)
    width, height = image.size
    ratio = 1000/width
    width *= ratio
    height *= ratio
    image = image.resize((int(width), int(height)))
    image.save('static/images/%s' % name, "JPEG", optimize=True)
    return name


def groupe(annee):
    janvier = False
    if 1 <= datetime.today().month < 9:
        janvier = True
    diff = datetime.today().year - annee
    if diff == 6:
        g = "GS"
    elif diff == 5:
        g = "MS" if janvier else "GS"
    elif diff == 4:
        g = "PS" if janvier else "MS"
    elif diff == 3:
        g = "TPS" if janvier else "PS"
    elif diff == 2:
        g = "TPS"
    else:
        g = "pb"
    return {"TPS": "Toute Petite Section", "PS": "Petite Section", "MS": "Moyenne Section",
            "GS": "Grande Section", "pb": "Maintien en GS"}[g]
