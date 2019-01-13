% rebase('base.tpl')
% from models import personnalise

<h1>{{enfant.prenom}} {{enfant.nom}} | {{enfant.date}}</h1>

<nav id="domaines">
    <ul>
    % for dom in domaines:
        <li><a href="/enfant/{{enfant.id}}/{{dom.id}}">{{dom.nom}}</a></li>
    % end
    </ul>
</nav>

<p>
    <a href="/commentaires/{{enfant.id}}" class="lien">Éditer les commentaires</a> |
    <a href="/bilan/{{enfant.id}}" class="lien">Générer le bilan</a> |
    <a href="/classe/{{enfant.annee}}/{{domaine.id}}" class="lien">Voir la classe</a>
</p>


<table>
    <tr>
        <th colspan="4">{{domaine.nom}}</th>
    </tr>
        % for index in sorted(domaine.competences.keys()):
        % competence = domaine.competences[index]
        <tr class="comp" id="competence_{{competence.id}}">
            <td colspan="4">{{competence.position}}. {{competence.nom}}</td>
        </tr>
        % for index2 in sorted(competence.observables.keys()):
        % observable = competence.observables[index2]
        <tr>
            <td>{{observable.position}}. {{personnalise(observable.nom, enfant.prenom, enfant.sexe)}}</td>
            <td id="{{enfant.id}}_{{observable.id}}" class="bouton {{observable.statut2}}">
                % if observable.date is not None:
                    {{observable.date}}
                % end
            </td>
            <td>
            % if observable.image_perso is not None :
                <p><img src="/static/images/{{observable.image_perso}}" alt="illustration" width="100"/></p>
            % elif observable.image is not None :
                <p><img src="/static/images/{{observable.image}}" alt="illustration" width="100"/></p>
            % else :
                <p><img src="/static/images/alt.png" alt="illustration" width="100"/></p>
            % end
            </td>
            <td>
            % if observable.image_perso is not None :
                <p>Modifier l'image personnelle:</p>
            % else :
                <p>Ajouter une image personnelle:</p>
            % end
                <form method="post" enctype="multipart/form-data" action="/upload_enfant">
                    <input name="enfant_id" value='{{enfant.id}}' type="hidden"/>
                    <input name="obs_id" value='{{observable.id}}' type="hidden"/>
                    <input name="dom_id" value='{{dom_id}}' type="hidden"/>
                    <input name="fichier" type="file"/>
                    <input type="submit" value="Envoyer"/>
                </form>
            % if observable.image_perso is not None :
                <p>Supprimer l'image personnelle:</p>
                <form method="post" action="/supp_image_enfant">
                    <input name="enfant_id" value='{{enfant.id}}' type="hidden"/>
                    <input name="obs_id" value='{{observable.id}}' type="hidden"/>
                    <input name="dom_id" value='{{dom_id}}' type="hidden"/>
                    <input type="submit" value="Supprimer"/>
                </form>
            % else :
			</td>
        % end
        </tr>
    % end
% end
</table>

<script src="/static/js/classe.js"></script>
