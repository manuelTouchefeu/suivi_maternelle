from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.colors import (
    black,
    darkgray,
    red,
)


def stylesheet():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Helvetica',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }
    styles['garde'] = ParagraphStyle(
        'garde',
        parent=styles['default'],
        fontSize=24,
        leading=24,
        textColor=black,
    )

    styles['nom'] = ParagraphStyle(
        'nom',
        parent=styles['default'],
        fontSize=18,
        leading=20,
        alignment=TA_RIGHT,
        textColor=black,
    )

    styles['dom'] = ParagraphStyle(
        'dom',
        parent=styles['default'],
        fontSize=18,
        leading=20,
        alignment=TA_LEFT,
        textColor=black,
    )

    styles['comp'] = ParagraphStyle(
        'comp',
        parent=styles['default'],
        fontSize=14,
        leading=15,
        alignment=TA_LEFT,
        textColor=black,
    )

    styles['suite'] = ParagraphStyle(
        'nom',
        parent=styles['default'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=darkgray,
    )

    styles['warning'] = ParagraphStyle(
        'nom',
        parent=styles['default'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        textColor=red,
    )

    styles['sep'] = ParagraphStyle(
        'sep',
        parent=styles['default'],
        alignment=TA_CENTER,
    )

    return styles
