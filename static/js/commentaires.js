(function toggle(){
    
    var modifier_boutons = document.querySelectorAll('.modifier_bouton');
    var annuler_boutons = document.querySelectorAll('.annuler');

    for (i=0, c=modifier_boutons.length; i<c; i++) {
        modifier_boutons[i].addEventListener('mouseup' , function() {
            this.parentNode.parentNode.previousElementSibling.style.display = 'block';
            this.parentNode.parentNode.parentNode.firstElementChild.style.display = 'none';
            this.parentNode.parentNode.style.display = 'none';
        }, false);
    }

    for (i=0, c=annuler_boutons.length; i<c; i++) {
        annuler_boutons[i].addEventListener('mouseup' , function() {
            this.parentNode.parentNode.style.display = 'none';
            this.parentNode.parentNode.parentNode.firstElementChild.style.display = 'block';
            this.parentNode.parentNode.nextElementSibling.style.display = 'block';
        }, false);
    }

})();
