% rebase('base_admin.tpl')

<h1>Utilisateurs</h1>
<ul>
% for u in users:
    <li id="{{u.id}}">{{u}} | {{u.login}} | <span class="staff">{{u.statut}}</span> | <span class="supp">X</span></li>
% end
</ul>

<h2>Ajouter un utilisateur:</h2>
    <form method="post" action="/ajoute_utilisateur">
        <label for="nom">Nom:</label> <br />
        <input id="nom" name="nom" type="text"/> <br />
        <label for="prenom">Prénom:</label> <br />
        <input id="prenom" name="prenom" type="text"/> <br />
        <label for="login">Login:</label> <br />
        <input id="login" name="login" type="text"/> <br />
        <label for="password">Mot de passe :</label> <br >
        <input id="password" name="password" type="text"/> <br />
        <label for="admin">Administrateur :</label>
        <input name="admin", id="admin", type="checkbox" value="1"/> <br />
        <br />
        <input id="submit" type="submit" value="Envoyer"/>
    </form>

<script src="/static/js/utilisateurs.js"></script>
