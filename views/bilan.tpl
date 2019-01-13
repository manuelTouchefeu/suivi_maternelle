% rebase('base.tpl')

<h1>{{enfant.prenom}} {{enfant.nom}} | {{enfant.date}}</h1>

<a href="/enfant/{{enfant.id}}/1" class="lien">Retour aux observables de {{enfant.prenom}}.</a>

<div class="formulaire">
    <p>Choisir les paramètres du bilan:</p>
    <form method="post" action="/pdf">
        <input type="hidden" id="id_enfant" name="id_enfant" value="{{enfant.id}}">
        <input type="checkbox" id="simple" name="simple" value="True">
        <label for="simple">Afficher seulement la dernière compétence acquise</label>
        <br>
        <input type="checkbox" id="warning" name="warning" value="True">
        <label for="warning">Afficher les difficultés</label>
        <br>
        <input type="checkbox" id="suite" name="suite" value="True">
        <label for="suite">Afficher les objectifs</label>
        <br>
        <input id="submit" type="submit" value="Envoyer"/>
    </form>
</div>