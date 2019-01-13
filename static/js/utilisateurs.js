"use strict";

var boutons, i, c;

function toggleAdmin(span) {
    span.addEventListener('mouseup' , function() {
        var user = span.parentNode.id;
        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/toggle_statut';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({user: user}));
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                span.innerText = xhr.responseText;
            }
        }, false);
    }, false);
}
boutons = document.getElementsByClassName("staff");
c=boutons.length;
for (i=0; i<c; i++) {
    toggleAdmin(boutons[i]);
}

function suppUser(span) {
    span.addEventListener('mouseup' , function() {
        var user = span.parentNode;
        var xhr = new XMLHttpRequest();
        // Envoi de la requête.
        var host = window.location.origin + '/supp_user';
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({user: user.id}));
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                user.parentNode.removeChild(user);
            }
        }, false);
    }, false);
}
boutons = document.getElementsByClassName("supp");
c=boutons.length;
for (i=0; i<c; i++) {
    suppUser(boutons[i]);
}