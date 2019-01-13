"use strict";

// Variables
var boutons, i, c;

// DÉPLACER une compétence
// Ajouter les eventListeners
function activeCloneComp(element) {
    var down = element.getElementsByClassName('down_comp')[0];
    down.addEventListener('mouseup', mdComp, false);
    var up = element.getElementsByClassName('up_comp')[0];
    up.addEventListener('mouseup', muComp, false);
    var edit = element.getElementsByClassName('edit')[0];
    editItem(edit)
    var sendModif = element.getElementsByClassName('sendEdit')[0];
    sendEdit(sendModif);
    var supp = element.getElementsByClassName('supp')[0];
    delComp(supp);
}
// Vérifier les flêches
function testPositionComp(element) {
    var down = element.getElementsByClassName('down_comp')[0];
    var up = element.getElementsByClassName('up_comp')[0];
    if (nextCompetence(element) == undefined) {
        down.style.display = 'none';
    }
    else {
        down.style.display = 'inline';
    }
    if (previousCompetence(element).className == 'head') {
        up.style.display = 'none';
    }
    else {
        up.style.display = 'inline';
    }
}

function nextCompetence(element) {
    var next = element.nextElementSibling;
    next = next.nextElementSibling;
    while(next != null && next.className != 'comp') {
        next = next.nextElementSibling;
    }
    return next;
}

function previousCompetence(element) {
    var previousComp = element.previousElementSibling;
    while(previousComp.className != 'head' && previousComp.className != 'comp') {
        previousComp = previousComp.previousElementSibling;
    }
    return previousComp;
}

function moveComp(comp) {
    var previousComp = previousCompetence(comp);
    var previousId = previousComp.id.split('_')[1];
    var currentId = comp.id.split('_')[1];
    var xhr = new XMLHttpRequest();
    // Envoi de la requête.
    var host = window.location.origin + '/move_comp';
    xhr.open('POST', host);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({up: currentId, down: previousId}));
    // Réception des données.
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === xhr.DONE) {
            var json = JSON.parse(xhr.responseText);

            var clone = comp.cloneNode(true);
            var clonesList = document.getElementsByClassName('comp_' + currentId);
            var c = clonesList.length;
            var clones = [];
            var clones2 = []; // des erreurs avec les boucles sur clonesList
            for(var i=0; i<c; i++) {
                clones.push(clonesList[i].cloneNode(true));
                clones2.push(clonesList[i]);
            }
            comp.parentNode.removeChild(comp);
            clones2.forEach(function(value, index, clones2) {
               value.parentNode.removeChild(value)
            });
            clone.getElementsByTagName('p')[0].innerText = json['up'];
            previousComp.getElementsByTagName('p')[0].innerText = json['down'];
            // Insérer la compétence et ses observables
            previousComp.parentNode.insertBefore(clone, previousComp);
            clones.forEach(function(value, index, clones) {
                previousComp.parentNode.insertBefore(value, previousComp);
                activeClone(value);
            });
            activeCloneComp(clone);
            testPositionComp(clone);
            testPositionComp(previousComp);
        }
    }, false);
}

function mdComp(e) {
    var currentId = e.target.id.split('_')[1];
    var currentComp = document.getElementById('comp_' + currentId);
    var nextComp = currentComp.nextElementSibling;
    while(nextComp.nextElementSibling.className != 'comp') {
        nextComp = nextComp.nextElementSibling;
    }
    nextComp = nextComp.nextElementSibling;
    moveComp(nextComp);
}
boutons = document.getElementsByClassName("down_comp");
c=boutons.length;
for (i=0; i<c; i++) {
    boutons[i].addEventListener('mouseup', mdComp, false);
}

function muComp(e) {
    var currentId = e.target.id.split('_')[1];
    var currentComp = document.getElementById('comp_' + currentId);
    moveComp(currentComp);
}
boutons = document.getElementsByClassName("up_comp");
c=boutons.length;
for (i=0; i<c; i++) {
    boutons[i].addEventListener('mouseup', muComp, false);
}

// MODIFIER le texte d'un observable ou d'une compétence
// Faire sortir le formulaire (pour observable ou compétence)
function editItem(bouton) {
    bouton.addEventListener('mouseup' , function() {
        this.parentNode.nextElementSibling.style.display = 'block';
        this.parentNode.style.display = 'none';
    }, false);
}
boutons = document.getElementsByClassName("edit");
c=boutons.length;
for (i=0; i<c; i++) {
    editItem(boutons[i]);
}
// Envoyer la modification et mettre à jour l'item -compétence ou observable
function sendEdit(bouton) {
    bouton.addEventListener('mouseup' , function() {
        //TODO: modifier l'ordre des choses.
        this.parentNode.previousElementSibling.style.display = 'block';
        this.parentNode.style.display = 'none';
        var itemValue = this.previousElementSibling.value;
        var itemType = bouton.id.split('.')[0];
        var itemId = bouton.id.split('.')[1];
        var xhr = new XMLHttpRequest();

        // Envoi de la requête.
        var host = window.location.origin + '/edit_item';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({id: itemId, text: itemValue, type: itemType}));

        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var json = JSON.parse(xhr.responseText);
                if (itemType == 'observable') {
                    var item = document.getElementById('obs_' + json['id']);
                }
                else {
                    var item = document.getElementById('competence_' + json['id']);
                }
                item.innerText = json['position'] + '. ' + json['text'];
            }
        }, false);

    }, false);
}
boutons = document.querySelectorAll(".modif input");
i, c=boutons.length;
for (i=0; i<c; i++) {
    sendEdit(boutons[i]);
}

// COMPETENCES ////////////////////////////////////////////////////////////////////////////////////////////////
// AJOUTER une compétence
// Sortir le formulaire
function compForm(bouton) {
    bouton.addEventListener('mouseup' , function() {
        this.parentNode.nextElementSibling.style.display = 'block';
    }, false);
}
boutons = document.getElementsByClassName("addComp");
c=boutons.length;
for (i=0; i<c; i++) {
    compForm(boutons[i]);
}

function addComp(bouton) {
    bouton.addEventListener('mouseup' , function() {
        this.parentNode.style.display = 'none';
        var competence = this.previousElementSibling.value
        var domId = this.id.split('.')[1];

        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/add_comp';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({dom: domId, text: competence}));

        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                //var json = JSON.parse(xhr.responseText);
                //var newObs = createObs(json['comp'], json['id'], json['position'], json['text']);
                document.location.reload();
            }
        }, false);
    }, false);
}
boutons = document.querySelectorAll(".send_comp input");
c=boutons.length;
for (i=0; i<c; i++) {
    addComp(boutons[i]);
}

// Supprimer une compétence
function delComp(bouton) {
    bouton.addEventListener('mouseup' , function() {
        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/del_comp';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({comp_id: bouton.id.split('_')[1]}));
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var json = JSON.parse(xhr.responseText);
                document.location.reload();
            }
        }, false);
    }, false);

}
boutons = document.querySelectorAll(".competence .supp");
c=boutons.length;
for (i=0; i<c; i++) {
    delComp(boutons[i]);
}

// OBSERVABLES ////////////////////////////////////////////////////////////////////////////////////////////////
// SUPPRIMER un observable
function delObs(bouton) {
    bouton.addEventListener('mouseup' , function() {
        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/del_obs';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({obs_id: bouton.id.split('_')[1]}));
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var json = JSON.parse(xhr.responseText);
                var ligne = document.querySelector('#observable_' + json['obs_id']);
                var compId = ligne.className.split('_')[1];
                ligne.parentNode.removeChild(ligne);

                for (var key in json) {
                    if (key != 'obs_id') {
                        var paragraph = document.getElementById('obs_' + key);
                        paragraph.textContent = json[key]['position'] + ". " + json[key]['text'];
                    }
                }
                // Vérifier les boutons
                var observables = document.getElementsByClassName('comp_'+compId);
                var i, c = observables.length;
                for (i=0; i<c; i++) {
                    testPosition(observables[i]);
                }
            }
        }, false);
    }, false);
}
boutons = document.querySelectorAll(".observable .supp");
c=boutons.length;
for (i=0; i<c; i++) {
    delObs(boutons[i]);
}

// DÉPLACER un observable
// Descendre un obs = monter le prochain
// Ajouter les eventListeners
function activeClone(element) {
    var down = element.getElementsByClassName('down')[0];
    down.addEventListener('mouseup', md, false);
    var up = element.getElementsByClassName('up')[0];
    up.addEventListener('mouseup', mu, false);
    var edit = element.getElementsByClassName('edit')[0];
    editItem(edit)
    var sendModif = element.getElementsByClassName('sendEdit')[0];
    sendEdit(sendModif);
    var supp = element.getElementsByClassName('supp')[0];
    delObs(supp);
    var update = element.getElementsByClassName('toggle')[0];
    updateObs(update);
}
// Vérifier les flêches
function testPosition(element) {
    var down = element.getElementsByClassName('down')[0];
    var up = element.getElementsByClassName('up')[0];
    if (element.nextElementSibling == undefined || element.nextElementSibling.className == "comp") {
        down.style.display = 'none';
    }
    else {
        down.style.display = 'inline';
    }
    if (element.previousElementSibling.className == "comp") {
        up.style.display = 'none';
    }
    else {
        up.style.display = 'inline';
    }
}

function move(currentObs) {
    var currentId = currentObs.id.split('_')[1];
    var previousObs = currentObs.previousElementSibling;
    var previousId = previousObs.id.split('_')[1];

    var xhr = new XMLHttpRequest();
    // Envoi de la requête.
    var host = window.location.origin + '/move_obs';
    xhr.open('POST', host);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({up: currentId, down: previousId}));
    // Réception des données.
    xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === xhr.DONE) {
            var json = JSON.parse(xhr.responseText);
            var clone = currentObs.cloneNode(true);
            clone.getElementsByTagName('p')[0].innerText = json['up'];
            previousObs.getElementsByTagName('p')[0].innerText = json['down'];
            currentObs.parentNode.removeChild(currentObs);
            previousObs.parentNode.insertBefore(clone, previousObs);
            testPosition(previousObs);
            testPosition(clone);
            activeClone(clone);
        }
    }, false);
}

function md(e) {
    var currentId = e.target.id.split('_')[1];
    var currentObs = document.getElementById('observable_' + currentId);
    var nextObs = currentObs.nextElementSibling;
    move(nextObs);
}
boutons = document.getElementsByClassName("down");
c=boutons.length;
for (i=0; i<c; i++) {
    boutons[i].addEventListener('mouseup', md, false);
}

function mu(e) {
    var currentId = e.target.id.split('_')[1];
    var currentObs = document.getElementById('observable_' + currentId);
    move(currentObs);
}
boutons = document.getElementsByClassName("up");
c=boutons.length;
for (i=0; i<c; i++) {
    boutons[i].addEventListener('mouseup', mu, false);
}

// AJOUTER un observable
function add(bouton) {
    bouton.addEventListener('mouseup' , function() {
        this.parentNode.nextElementSibling.nextElementSibling.style.display = 'block';
    }, false);
}
boutons = document.getElementsByClassName("add");
c=boutons.length;
for (i=0; i<c; i++) {
    add(boutons[i]);
}

function createObs(compId, id, position, text) {
    var newObs = document.createElement('tr');
    newObs.id = "observable_" + id;
    newObs.className = "comp_" + compId;
    var td1 = document.createElement('td');
    var td2 = document.createElement('td');
    var td3 = document.createElement('td');
    var td4 = document.createElement('td');
    //td1
    var observable = document.createElement('div');
    observable.className = 'observable';
    var nom = document.createElement('p');
    nom.id = 'obs_' + id;
    nom.innerText = position + ". " + text;
    observable.appendChild(nom);
    var up = document.createElement('span');
    up.className = 'bouton_obs up';
    up.innerText = '↑ ';
    up.id = 'up_' + id;
    observable.appendChild(up);
    up.addEventListener('mouseup', mu, false);
    var down = document.createElement('span');
    down.className = 'bouton_obs down';
    down.innerText = '↓ ';
    down.id = 'down_' + id;
    down.style.display = 'none';
    observable.appendChild(down);
    down.addEventListener('mouseup', md, false);
    var edit = document.createElement('span');
    edit.className = 'bouton_obs edit';
    edit.id = 'edit_' + id;
    edit.innerText = '⥁ ';
    editItem(edit);
    observable.appendChild(edit);
    var supp = document.createElement('span');
    supp.className = 'bouton_obs supp';
    supp.id = 'supp_' + id;
    supp.innerText = 'x ';
    delObs(supp);
    observable.appendChild(supp);
    td1.appendChild(observable);

    var modif = document.createElement('div');
    modif.className = 'modif';
    var saisie = document.createElement('textarea');
    saisie.innerText = text;
    modif.appendChild(saisie);
    var send = document.createElement('input');
    send.type = 'button';
    send.id = 'observable.' + id;
    send.value = 'valider';
    send.className = 'sendEdit';
    sendEdit(send);
    modif.appendChild(send);
    td1.appendChild(modif);
    newObs.appendChild(td1);

    //td2
    td2.className = 'toggle petit';
    td2.id = id;
    td2.innerText = '2-4,5 ans';
    updateObs(td2);
    newObs.appendChild(td2);

    //td3
    td3.innerHTML = "<p><img src=\"/static/images/alt.png\" alt=\"illustration\" width=\"100\"/></p>";
    newObs.appendChild(td3);

    //td4
    td4.innerHTML =
        "<form method=\"post\" enctype=\"multipart/form-data\" action=\"/upload\">" +
            "<input name=\"dom_id\" value=\"" + id + "\" type=\"hidden\"/>" +
            "<input name=\"obs_id\" value=\"" + id + "\" type=\"hidden\"/>" +
            "<input name=\"fichier\" type=\"file\" required/>" +
            "<input type=\"submit\" value=\"Envoyer\"/>" +
        "</form>";
    newObs.appendChild(td4);
    return newObs;
}

function addObs(bouton) {
    bouton.addEventListener('mouseup' , function() {
        this.parentNode.style.display = 'none';
        var observable = this.previousElementSibling.value;
        this.previousElementSibling.value = '';
        var compId = this.id.split('.')[1];
        // Trouver la prochaine compétence.
        var currentComp = document.getElementById('comp_' + compId);
        var element = currentComp.nextElementSibling;
        var lastObs = element;
        while (element != null && element.className != 'comp') {
            lastObs = element;
            element = element.nextElementSibling;
        }
        if (element == null) {
            var dernier = true;
        }
        else {
            var dernier = false;
            var nextComp = element;
        }

        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/add_obs';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({comp: bouton.id.split('.')[1], text: observable}));

        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var json = JSON.parse(xhr.responseText);
                var newObs = createObs(json['comp'], json['id'], json['position'], json['text']);

                if (dernier == false) {
                    nextComp.parentNode.insertBefore(newObs, nextComp);
                }
                else {
                    currentComp.parentNode.appendChild(newObs);
                }

                //ajouter le bouton down à l'avant-dernier observable !!!!!
                if (lastObs != undefined) {
                    testPosition(lastObs);
                }

            }
        }, false);

    }, false);
}
boutons = document.querySelectorAll(".add_comp input");
c=boutons.length;
for (i=0; i<c; i++) {
    addObs(boutons[i]);
}

// NIVEAU des observables
function updateObs(bouton) {
    bouton.addEventListener('mouseup' , function() {

        var niveau = 0;
        if (bouton.classList.contains('grand')) {
            niveau = 2;
        }
        else if (bouton.classList.contains('moyen')) {
            niveau = 1;
        }

        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/update_niveau'
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send('var=' + bouton.id + '_' + niveau);
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var response = xhr.responseText
                if (response == '2'){
                    bouton.className = 'toggle grand';
                    bouton.textContent = '5-6 ans';
                }
                else if (response == '1'){
                    bouton.className = 'toggle moyen';
                    bouton.textContent = '4-5 ans';
                }
                else if (response == '0'){
                    bouton.className = 'toggle petit';
                    bouton.textContent = '2-4 ans';
                }
            }
        }, false);

    }, false);
}
boutons = document.getElementsByClassName("toggle");
c=boutons.length;
for (i=0; i<c; i++) {
    updateObs(boutons[i]);
}