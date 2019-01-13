% rebase('base.tpl')
% from models import groupe

<h1>Classes</h1>

<table>
    <tr>
        % for annee in sorted(enfants.keys(), reverse=True):
            <th><a href="classe/{{annee}}/1">{{groupe(annee)}}</a></th>
        % end
    </tr>
    <tr>
        % for annee in sorted(enfants.keys(), reverse=True):
        <td>
            <ul>
            % for enfant in enfants[annee]:
                <li id="{{enfant.id}}">
                <a href="enfant/{{enfant.id}}/1" class="enfant_classe">{{enfant.nom}} {{enfant.prenom}} ({{enfant.date}})</a>
                | <span class="supp">X</span>
                </li>
            % end
            </ul>
        </td>
        % end
    </tr>
</table>

<div class="conteneur">
    <div class="formulaire">
        <h2>Ajouter un enfant:</h2>
        <form method="post" action="/ajoute_enfant">
            <label for="nom">Nom:</label> <br />
            <input id="nom" name="nom" type="text"/> <br />
            <label for="prenom">Prénom:</label> <br />
            <input id="prenom" name="prenom" type="text"/> <br />
            <label for="date">Date de naissance:</label> <br />
            <input id="date" name="date" type="text" placeholder="jj/mm/aaaa"/> <br />
            <label for="sexe">Sexe :</label>
            <select id="sexe" name="sexe">
                <option value="F">F</option>
                <option value="M">M</option>
            </select> <br />
            <br />
            <input id="submit" type="submit" value="Envoyer"/>
        </form>
    </div>
</div>

<script src="/static/js/classes.js"></script>

