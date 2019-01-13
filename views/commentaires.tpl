% rebase('base.tpl')

<h1>{{enfant.prenom}} {{enfant.nom}} | {{enfant.date}}</h1>


    <a href="/enfant/{{enfant.id}}/1" class="lien">Retour aux observables de {{enfant.prenom}}.</a>


% if len(enfant.commentaires) == 0:
    <p>Il n'y a pas encore de commentaires.</p>
% else:
    % for commentaire in enfant.commentaires:
        <div class="commentaire">
            <div>
                <p>
                    % for ligne in commentaire.texte.split("\n"):
                        {{ligne}} <br>
                    % end  
                    (Le {{commentaire.date}})
                </p>
            </div>
            <div class="modifier_form">
                <form method="post" action="/update_com">
                    <textarea id="texte" name="texte" rows="10" cols="50">{{commentaire.texte}}</textarea>
                    <input id="id_enfant" name="id_enfant" type="hidden" value={{enfant.id}}> <br />
                    <input id="id_com" name="id_com" type="hidden" value={{commentaire.id_com}}> <br />
                    <input id="submit" type="submit" value="Modifier"/>
                    <input id="annuler" class="annuler" type="button" value="Annuler"/>
                </form>
            </div>
            <div class="boutons">
                <p><span class="modifier_bouton" id="modifier_bouton_{{commentaire.id_com}}">Modifier</span> | <a href="/supp_com/{{commentaire.id_com}}/{{enfant.id}}">Supprimer</a><p/>
            </div>
        </div>
    %end
% end


<div class="formulaire">
    <h2>Ajouter un commentaire:</h2>
    <form method="post" action="/ajout_com">
        <textarea id="texte" name="texte" rows="10" cols="50"></textarea> <br />
        <input id="id_enfant" name="id_enfant" type="hidden" value={{enfant.id}}> <br />
        <input id="submit" type="submit" value="Envoyer"/>
    </form>
</div>

<script src="/static/js/commentaires.js"></script>
