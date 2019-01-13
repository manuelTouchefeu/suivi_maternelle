% rebase('base.tpl')

<h1>Observables</h1>

<nav id="domaines">
    <ul>
    % for elt in dom:
        <li><a href="/observables/{{elt.id}}">{{elt.nom}}</a></li>
    % end
    </ul>
</nav>


    <table>
        <tr class="head">
            <th colspan="4">
                <div class="domaine">
                    {{domaine.id}}. {{domaine.nom}}
                    <span class="bouton_comp addComp">+</span>
                </div>
                <div class="send_comp">
                    <textarea></textarea>
                    <input type="button" id="dom.{{domaine.id}}" value="valider">
                </div>
            </th>
        </tr>
        % for index in sorted(domaine.competences.keys()):
        % comp = domaine.competences[index]
            <tr id="comp_{{comp.id}}" class="comp">
                <td colspan="4">
                    <div class="competence">
                        <p id="competence_{{comp.id}}">{{comp.position}}. {{comp.nom}}</p>
                        % if comp.position != 1:
                            <span id="up_{{comp.id}}" class="bouton_comp up_comp">↑ </span>
                        % else:
                            <span id="up_{{comp.id}}" class="bouton_comp up_comp" style="display: none">↑ </span>
                        % end
                        % if comp.position+1 in domaine.competences.keys():
                            <span id="down_{{comp.id}}" class="bouton_comp down_comp">↓ </span>
                        % else:
                            <span id="down_{{comp.id}}" class="bouton_comp down_comp" style="display: none">↓ </span>
                        % end
                        <span id="edit_{{comp.id}}" class="bouton_comp edit">⥁ </span>
                        <span id="supp_{{comp.id}}" class="bouton_comp supp">x</span>
                        <span class="bouton_comp add">+</span>
                    </div>
                    <div class="modif">
                        <textarea>{{comp.nom}}</textarea>
                        <input type="button" id="competence.{{comp.id}}" class="sendEdit" value="valider">
                    </div>
                    <div class="add_comp">
                        <textarea></textarea>
                        <input type="button" id="comp.{{comp.id}}" value="valider">
                    </div>
                </td>
            </tr>
            % for index2 in sorted(comp.observables.keys()):
            % obs = comp.observables[index2]
            <tr id="observable_{{obs.id}}" class="comp_{{comp.id}}">
                <td>
                    <div class="observable">
                        <p id="obs_{{obs.id}}">{{obs.position}}. {{obs.nom}}</p>
                        % if obs.position != 1:
                            <span id="up_{{obs.id}}" class="bouton_obs up">↑ </span>
                        % else:
                            <span id="up_{{obs.id}}" class="bouton_obs up" style="display: none">↑ </span>
                        % end
                        % if obs.position+1 in comp.observables.keys():
                            <span id="down_{{obs.id}}" class="bouton_obs down">↓ </span>
                        % else:
                            <span id="down_{{obs.id}}" class="bouton_obs down" style="display: none">↓ </span>
                        % end
                        <span id="edit_{{obs.id}}" class="bouton_obs edit">⥁ </span>
                        <span id="supp_{{obs.id}}" class="bouton_obs supp">x</span>
                    </div>
                    <div class="modif">
                        <textarea>{{obs.nom}}</textarea>
                        <input type="button" id="observable.{{obs.id}}" class="sendEdit", value="valider">
                    </div>
                </td>
                % if obs.niveau == 0:
                    <td class="toggle petit" id="{{obs.id}}">2-4 ans</td>
                % elif obs.niveau == 1:
                    <td class="toggle moyen" id="{{obs.id}}">4-5 ans</td>
                % else:
                    <td class="toggle grand" id="{{obs.id}}">5-6 ans</td>
                % end
                <td>
                % if obs.image is not None:
                    <p><img src="/static/images/{{obs.image}}" alt="illustration" width="100" /></p>
                % else:
                    <p><img src="/static/images/alt.png" alt="illustration" width="100" /></p>
                % end
                </td>
                <td>
                <form method="post" enctype="multipart/form-data" action="/upload">
                    <input name="dom_id" value='{{dom_id}}' type="hidden"/>
                    <input name="obs_id" value='{{obs.id}}' type="hidden"/>
                    <input name="fichier" type="file" required/>
                    <input type="submit" value="Envoyer"/>
                </form>
                % if obs.image is not None :
                <p>Supprimer l'image:</p>
                <form method="post" action="/supp_image">
                    <input name="obs_id" value='{{obs.id}}' type="hidden"/>
                    <input name="dom_id" value='{{dom_id}}' type="hidden"/>
                    <input type="submit" value="Supprimer"/>
                </form>
                % end
            % else :
                </td>
            </tr>
        % end
    % end
    </table>


<script src="/static/js/observables.js"></script>
