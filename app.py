#!env/bin/python3
from bottle import default_app, route, template, response, static_file, error, redirect, run
from models import *
import json
from datetime import datetime
from pdf import build_pdf


# LOGIN ET SESSIONS____________________________________________________________________________________________________
def login_required(fn):
    def check(**kwargs):
        user = UserManager().is_user_test()
        if user:
            kwargs['user'] = user
            return fn(**kwargs)            
        else:
            redirect('/login')
            
    return check


@route('/login')
def login():
    return template('login.tpl')


@route('/login_form', method='POST')
def login_form():
    log = request.forms.login
    password = request.forms.password
    user = UserManager().authentication(log, password)
    if user:
        response.set_cookie('user', str(user.id), secret='some-secret-key', max_age=700000)  # max_age=600
        redirect('/')
    redirect('/login')


@route('/logout')
def logout():
    response.delete_cookie('user')
    redirect('/login')


# AFFICHAGE ET GESTION DES CLASSES ET DES ÉLÈVES ______________________________________________________________________
@route('/')
@route('/classes')
@login_required
def classes(**kwargs):
    enfants = EnfantManager().get_enfants()
    dictionnaire = {}
    for e in enfants:
        if e.annee not in dictionnaire.keys():
            dictionnaire[e.annee] = [e]
        else:
            dictionnaire[e.annee].append(e)
    return template('classes.tpl', enfants=dictionnaire, user=kwargs['user'])


@route('/ajoute_enfant', method='POST')
def ajoute_enfant():
    nom = request.forms.nom
    prenom = request.forms.prenom
    sexe = request.forms.sexe
    date = request.forms.date
    jour, mois, annee = date.split('/')
    date_n = datetime(int(annee), int(mois), int(jour)).timestamp()
    EnfantManager().add_enfant(nom, prenom, sexe, date_n)
    redirect('/classes')


@route('/supp_enfant', method='POST')
def supp_enfant():
    id_enfant = request.json['enfant']
    return EnfantManager().supp_enfant(int(id_enfant))


# GESTION D'UNE CLASSE ________________________________________________________________________________________________
@route('/classe/<annee>/<id_dom>')
@login_required
def classe(annee, id_dom, **kwargs):
    liste = EnfantManager().get_classe(annee, id_dom)
    manager = DomaineManager()
    domaines = manager.get_domaines()
    domaine = manager.get_observables_dom(id_dom)
    return template('classe.tpl', domaines=domaines, annee=annee, liste=liste, domaine=domaine, user=kwargs['user'])


@route('/valider', method='POST')
def valider():
    id_enfant, id_obs, but = request.params.get('var').split('_')
    if but == '1':  # valider
        date = datetime.today()
        EnfantManager().valide(int(id_enfant), int(id_obs), date.timestamp())
        return "%d/%d/%d" % (date.day, date.month, date.year)
    elif but == '0':  # annuler
        EnfantManager().annule_obs_enfant(int(id_obs), int(id_enfant))
        age = EnfantManager().get_enfant(int(id_enfant)).age
        niveau = DomaineManager().get_observable(int(id_obs)).niveau
        if age == niveau:
            return '2'
        elif age > niveau:
            return '1'
        elif niveau > age:
            return '3'
    return 'Erreur!'


# GESTION D'UN ENFANT _________________________________________________________________________________________________
@route('/enfant/<id_enfant>/<id_dom>')
@login_required
def enfant(id_enfant, id_dom, **kwargs):
    enf = EnfantManager().get_enfant(int(id_enfant), id_dom=id_dom)
    domaines = DomaineManager().get_domaines()
    return template('enfant.tpl', enfant=enf, domaine=enf.observables, domaines=domaines,
                    dom_id=id_dom, user=kwargs['user'])


@route('/upload_enfant', method='POST')
def upload_image_enfant():
    observable_id = int(request.forms.obs_id)
    enfant_id = int(request.forms.enfant_id)
    file = request.files.get('fichier')
    name = process_image(file, observable_id, enfant_id)
    if name:
        EnfantManager().update_enfant_image(enfant_id, observable_id, name)
    redirect('/enfant/%s/%s' % (enfant_id, request.forms.dom_id))


@route('/supp_image_enfant', method='POST')
def supp_image_enfant():
    enfant_id = int(request.forms.enfant_id)
    EnfantManager().supp_enfant_image(enfant_id, request.forms.obs_id)
    redirect('/enfant/%s/%s' % (enfant_id, request.forms.dom_id))


@route('/commentaires/<id_enfant>')
@login_required
def commentaires(id_enfant, **kwargs):
    child = EnfantManager().get_enfant(int(id_enfant))
    return template('commentaires.tpl', enfant=child, user=kwargs['user'])


@route('/ajout_com', method='POST')
def ajout_commentaire():
    id_enfant = request.forms.id_enfant
    texte = request.forms.texte
    texte = texte.replace("'", "’")
    date = datetime.today().timestamp()
    EnfantManager().add_commentaire(id_enfant, texte, date)
    redirect('/commentaires/%s' % id_enfant)


@route('/supp_com/<id_com>/<id_enfant>')
def supp_commentaire(id_com, id_enfant):
    EnfantManager().supp_commentaire(id_com)
    redirect('/commentaires/%s' % id_enfant)


@route('/update_com', method='POST')
def update_commentaire():
    id_com = request.forms.id_com
    texte = request.forms.texte.replace("'", "’")
    id_enfant = request.forms.id_enfant
    EnfantManager().update_commentaire(id_com, texte)
    redirect('/commentaires/%s' % id_enfant)


# PDF _________________________________________________________________________________________________________________
@route('/bilan/<id_enfant>')
@login_required
def bilan(id_enfant, **kwargs):
    e = EnfantManager().get_enfant(int(id_enfant))
    return template('bilan.tpl', enfant=e, user=kwargs['user'])


@route('/pdf', method='POST')
def create_pdf():
    """Générer le bilan d'un enfant sous la forme d'un pdf"""
    id_enfant = request.forms.id_enfant
    req = request.forms.__dict__['dict']
    simple = True if 'simple' in req.keys() else False
    warning = True if 'warning' in req.keys() else False
    suite = True if 'suite' in req.keys() else False
    child = EnfantManager().get_enfant(int(id_enfant))
    domaines = DomaineManager().get_domaines()
    obs = []
    for domaine in domaines:
        if domaine.nom != "Compétences transversales":
            obs.append(EnfantManager().get_domaine_enfant(child, domaine.id))
    filename = '%s_%s.pdf' % (child.nom, child.prenom)
    path = 'static/pdf/'
    build_pdf('{}{}'.format(path, filename), child, obs,
              simple=simple,
              warning=warning,
              suite=suite)
    return static_file(filename, root=path, mimetype='application/pdf')


# GESTION DES OBSERVABLES _____________________________________________________________________________________________
@route('/observables/<id_dom>')
@login_required
def observables(id_dom, **kwargs):
    manager = DomaineManager()
    dom = manager.get_domaines()
    domaine = manager.get_observables_dom(id_dom)
    return template('observables.tpl', dom=dom, domaine=domaine, dom_id=id_dom, user=kwargs['user'])


@route('/update_niveau', method='POST')
def update_niveau():  
    id_obs, niveau = request.params.get('var').split('_')
    if niveau == '2':
        DomaineManager().niveau_observable(int(id_obs), 0)
        return '0'
    else:
        DomaineManager().niveau_observable(int(id_obs), int(niveau)+1)
        return str(int(niveau)+1)


@route('/edit_item', method='POST')
def edit_item():
    data = request.json
    manager = DomaineManager()
    manager.update_text(int(data['id']), data['text'], data['type'])
    item = None
    if data['type'] == 'observable':
        item = manager.get_observable(int(data['id']))
    elif data['type'] == 'competence':
        item = manager.get_competence(int(data['id']))
    return json.dumps({"id": item.id, "position": item.position, "text": item.nom})


@route('/add_obs', method='POST')
def add_obs():
    data = request.json
    obs = DomaineManager().add_obs(int(data["comp"]), data["text"])
    return json.dumps({"comp": obs.competence, "text": obs.nom, "id": obs.id, "position": obs.position})


@route('/del_obs', method='POST')
def del_obs():
    data = request.json
    modif = {}
    for obs in DomaineManager().del_obs(int(data["obs_id"])):
        modif[obs.id] = {'position': obs.position, 'text': obs.nom}
    modif['obs_id'] = data["obs_id"]
    return json.dumps(modif)


@route('/del_comp', method='POST')
def del_comp():
    data = request.json
    modif = {}
    for comp in DomaineManager().del_comp(int(data["comp_id"])):
        modif[comp.id] = {'position': comp.position, 'text': comp.nom}
    modif['comp_id'] = data["comp_id"]
    return json.dumps(modif)


@route('/move_obs', method='POST')
def move_obs():
    data = request.json
    obs = DomaineManager().update_position(int(data['up']), int(data['down']))
    up = '%d. %s' % (obs['up'].position, obs['up'].nom)
    down = '%d. %s' % (obs['down'].position, obs['down'].nom)
    return json.dumps({'up': up, 'down': down})


@route('/move_comp', method='POST')
def move_comp():
    data = request.json
    comp = DomaineManager().update_position_comp(int(data['up']), int(data['down']))
    up = '%d. %s' % (comp['up'].position, comp['up'].nom)
    down = '%d. %s' % (comp['down'].position, comp['down'].nom)
    return json.dumps({'up': up, 'down': down})


@route('/upload', method='POST')
def observables_upload():
    """ Upload des illustrations des observables """
    observable_id = request.forms.obs_id
    file = request.files.get('fichier')
    name = process_image(file, observable_id)
    if name:
        DomaineManager().add_image_obs(observable_id, name)
    redirect('/observables/%s' % request.forms.dom_id)


@route('/supp_image', method='POST')
def supp_image():
    DomaineManager().supp_image(request.forms.obs_id)
    redirect('/observables/%s' % request.forms.dom_id)


@route('/add_comp', method='POST')
def add_comp():
    data = request.json
    comp = DomaineManager().add_comp(int(data["dom"]), data["text"])
    return json.dumps({"text": comp.nom, "id": comp.id, "position": comp.position})


# ADMIN ________________________________________________________________________________________________________
def is_staff_required(fn):
    def check(**kwargs):
        user = UserManager().is_staff_test()
        if user is None:
            redirect('/logout')
        else:
            kwargs['user'] = user
            return fn(**kwargs)
    return check


@route('/admin')
@is_staff_required
def utilisateurs(**kwargs):
    return template('utilisateurs.tpl', user=kwargs['user'], users=UserManager().get_users())


@route('/ajoute_utilisateur', method='POST')
def ajoute_utilisateur():
    nom = request.forms.nom
    prenom = request.forms.prenom
    log = request.forms.login
    password = request.forms.password
    is_staff = 1 if request.forms.admin == '1' else 0
    UserManager().add_user(nom, prenom, log, password, is_staff)
    redirect('/admin')


@route('/toggle_statut', method='POST')
def toggle_statut():
    return UserManager().toggle_statut(int(request.json['user'])).statut


@route('/supp_user', method='POST')
def supp_user():
    return UserManager().supp_user(int(request.json['user']))


# DIVERS ______________________________________________________________________________________________________________
# static files
@route('/static/<filename:path>')
def send_static_file(filename):
    return static_file(filename, root='./static')


# 404
@error(404)
def error404(error):
    return template('404.tpl', user=UserManager().is_user_test())


# favicon
@route('/favicon.ico', method='GET')
def get_favicon():
    return static_file('favicon.png', root='./static/icones')


app = default_app()
# run(server='gunicorn', workers=4, reloader=True, debug=True, host='0.0.0.0', port=80)
if __name__ == '__main__':
    run(reloader=True, debug=True, host='0.0.0.0', port=8080)
