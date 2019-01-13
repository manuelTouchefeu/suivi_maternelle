% rebase('base.tpl')
% from models import groupe

<h1>{{groupe(int(annee))}}</h1>

<nav id="domaines">
    <ul>
    % for dom in domaines:
        <li><a href="/classe/{{annee}}/{{dom.id}}">{{dom.nom}}</a></li>
    % end
    </ul>
</nav>

<table>
    <tr>
        <th>{{domaine.nom}}</th>
        % for enfant in liste:
            <th><a href="/enfant/{{enfant.id}}/{{domaine.id}}">{{enfant.prenom}} {{enfant.nom[0]}}.</a></th>
        % end
    </tr>

    % for index in sorted(domaine.competences.keys()):
    % comp = domaine.competences[index]
            <tr class="competence">
                <td><strong>{{comp.position}}. {{comp.nom}}</strong></td>
                % for enfant in liste:
                    <td><strong><a href="/enfant/{{enfant.id}}/{{domaine.id}}#competence_{{comp.id}}">{{enfant.prenom}}</a></strong></td>
                % end
            </tr>
            % for index2 in sorted(comp.observables.keys()):
            % obs = comp.observables[index2]
                <tr>
                    <td class="obs">{{obs.position}}. {{obs.nom}}</td>
                    % for enfant in liste:
                        % obs_enfant = enfant.observables.competences[comp.position].observables[obs.position]
                        <td id="{{enfant.id}}_{{obs.id}}" class="bouton {{obs_enfant.statut2}}">
                            % if obs_enfant.date is not None:
                                {{obs_enfant.date}}
                            % end
                        </td>
                        % end
                    % end
                </tr>
            % end
    % end
</table>

<script src="/static/js/classe.js"></script>
