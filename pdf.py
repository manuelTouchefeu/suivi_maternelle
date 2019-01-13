from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    PageBreak,
    FrameBreak,
    Image,
    KeepTogether
)
from reportlab.lib.units import cm
from pdf_style import *
from datetime import datetime
from models import personnalise


def im(path, doc):
    largeur = doc.width/2 - doc.leftMargin/2
    with open(path, 'rb') as image: # l'image est fermée à la fin.
        im1 = Image(image)
        if im1.imageWidth == im1.imageHeight:
            hauteur = largeur
        if im1.imageWidth > im1.imageHeight:
            ratio = im1.imageWidth / im1.imageHeight
            hauteur = largeur / ratio
        else:
            ratio = im1.imageHeight / im1.imageWidth
            hauteur = largeur * ratio
    return Image(path, width=largeur, height=hauteur)


def build_pdf(filename, enfant, observables, simple=True, warning=True, suite=True):
    """Construction du pdf."""
    # Ajouter:
    # Toutes les compétences acquises -> simple = False
    # OU la dernière compétence acquise -> simple = True
    # Signaler ou pas les compétences qui devraient être acquises -> warning = True ou warning = False
    # Ajouter ou pas la prochaine compétence à acquérir -> suite = True ou suite = False
    doc = BaseDocTemplate(filename,
                          leftMargin=1*cm,
                          rightMargin=1*cm,
                          topMargin=1*cm,
                          bottomMargin=1*cm,
                          title="%s_%s" % (enfant.nom, enfant.prenom),)
    column_gap = 0.5 * cm
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width / 2,
                        doc.height,
                        id='left',
                        # rightPadding=column_gap / 2,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + doc.width / 2,
                        doc.bottomMargin,
                        doc.width / 2,
                        doc.height,
                        id='right',
                        # leftPadding=column_gap / 2,
                        showBoundary=0
                    ),
                ]
            ),
        ]
    )

    flowables = list()

    # Page de garde
    flowables.append(Paragraph("Livret de suivi des apprentissages", stylesheet()['garde']),)
    flowables.append(Spacer(0, cm * 0.5))
    date = datetime.today()
    flowables.append(Paragraph("Édité le %d/%d/%d" % (date.day, date.month, date.year), stylesheet()['default']),)
    flowables.append(Spacer(0, cm * 23))
    flowables.append(Paragraph("École de Teuillac", stylesheet()['dom']),)
    flowables.append(FrameBreak())

    string = '%s %s\n(%s)' % (enfant.prenom, enfant.nom, enfant.date)
    flowables.append(Paragraph(string, stylesheet()['nom']),)
    flowables.append(Spacer(0, cm * 24))

    # Suite
    for dom in observables:
        flowables.append(PageBreak())
        flowables.append(Paragraph("<b>%s</b>" % dom.nom, stylesheet()['dom']),)
        flowables.append(Spacer(0, cm * .3))

        for index in sorted(dom.competences.keys()):
            competence = dom.competences[index]
            # len_comp = len(competence.observables)
            first = [Paragraph("<b>%s</b>" % competence.nom, ParagraphStyle('comp')), Spacer(0, cm * .3)]
            for index2 in sorted(competence.observables.keys()):
                observable = competence.observables[index2]
                if observable.statut != 0 and observable.statut != 1:
                    break
                if warning is False and observable.statut == 1:
                    break
                if simple is True and index2+1 in competence.observables.keys()\
                        and competence.observables[index2+1].statut == 0:
                    continue

                obs = Paragraph("→ %s" %
                                personnalise(observable.nom, enfant.prenom, enfant.sexe), stylesheet()['default'])
                if warning is True and observable.statut == 1:
                    obs = Paragraph("!! %s" % observable.nom, stylesheet()['warning'])

                path = None
                #print('%s, %s' % (observable.image, observable.image_perso))
                if observable.image_perso is not None:
                    path = "static/images/%s" % observable.image_perso
                elif observable.image is not None:
                    path = "static/images/%s" % observable.image

                if path is not None and observable.statut == 0:
                    if simple is True or observable.position == 1:
                        ajout = KeepTogether(first + [obs, im(path, doc)])
                    else:
                        ajout = KeepTogether([obs, im(path, doc)])
                else:
                    if warning is True and observable.statut == 1 and observable.position != 1:
                        ajout = obs
                    elif simple is True or observable.position == 1:
                        ajout = KeepTogether(first + [obs])
                    else:
                        ajout = obs
                flowables.append(ajout)
                flowables.append(Spacer(0, cm * .3))

                # Ajouter la perspective
                if suite is True\
                        and index2+1 in competence.observables.keys()\
                        and observable.statut != 1:
                    observable2 = competence.observables[index2+1]
                    if warning is True and observable2.statut == 1:
                        pass
                    elif observable2.statut != 0:
                        obs = Paragraph("%s" % personnalise(observable2.nom, enfant.prenom, enfant.sexe),
                                        stylesheet()['suite'])
                        flowables.append(obs)
                        flowables.append(Spacer(0, cm * .3))
    # Commentaires
    flowables.append(PageBreak())
    for commentaire in enfant.commentaires:
        flowables.append(Paragraph(commentaire.texte, stylesheet()['default']),)
        flowables.append(Spacer(0, cm * .3))
    doc.build(flowables)
