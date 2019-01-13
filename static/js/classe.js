"use strict";

function updateObs(bouton) {
    bouton.addEventListener('mouseup' , function() {

        var xhr = new XMLHttpRequest();
        var but = bouton.classList.contains('ok') ? 0 : 1;
        // Envoi de la requête.
        var host = window.location.origin + '/valider'
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send('var=' + bouton.id + '_' + but);
        // xhr.send(JSON.stringify({enfant: id_enfant}));

        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                var response = xhr.responseText
                if (but == 1){
                    bouton.className = 'bouton ok'
                    bouton.textContent = response;
                }
                else {
                    switch (response) {
                        case '2': bouton.className = 'bouton suite';
                        break;
                        case '1': bouton.className = 'bouton alerte';
                        break;
                        case '3': bouton.className = 'bouton passe';
                        break;
                        default:
                            bouton.className = 'bouton passe';
                    }
                    bouton.textContent = ''
                }
            }
        }, false);

    }, false);
}

var boutons = document.getElementsByClassName("bouton");

for (var i=0, c=boutons.length; i<c; i++) {
    updateObs(boutons[i]);
}
