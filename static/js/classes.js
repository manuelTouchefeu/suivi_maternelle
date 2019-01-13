function suppEnfant(bouton) {
    bouton.addEventListener('mouseup' , function() {
        var liste = bouton.parentNode.parentNode
        var id_enfant = bouton.parentNode.id;
        var nom = bouton.parentNode.getElementsByTagName('a')[0].innerText;
        if (!confirm('Un accident est vite arrivé. Supprimer ' + nom +'?')) {
            return;
        }
        var xhr = new XMLHttpRequest();
        var host = window.location.origin + '/supp_enfant'
        xhr.open('POST', host);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({enfant: id_enfant}));
        // Réception des données.
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === xhr.DONE) {
                liste.removeChild(bouton.parentNode);
            }
        }, false);

    }, false);
}

var boutons = document.getElementsByClassName("supp");

for (i=0, c=boutons.length; i<c; i++) {
    suppEnfant(boutons[i]);
}
