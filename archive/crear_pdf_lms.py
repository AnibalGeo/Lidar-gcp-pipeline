# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os

IMG_DIR  = r'C:\Users\amata\Desktop\Google\docx_images'
LOGO_IMG = os.path.join(IMG_DIR, 'image1.png')
OUT_PDF  = r'C:\Users\amata\Desktop\Google\LMS-BestPractice-Vuelo-Produccion-ES.pdf'

PAGE_W, PAGE_H = A4
MARGIN    = 2.0 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

BLUE_DARK  = colors.HexColor('#1F3864')
BLUE_MID   = colors.HexColor('#2980B9')
BLUE_LIGHT = colors.HexColor('#EBF5FB')
GREY_LINE  = colors.HexColor('#BDC3C7')

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(base_name, **kw):
    parent = styles.get(base_name) or styles['Normal']
    return ParagraphStyle('_' + base_name + str(id(kw)), parent=parent, **kw)

normal   = S('Normal', fontSize=10, leading=15, spaceAfter=6, alignment=TA_JUSTIFY)
section  = S('Normal', fontSize=13, leading=17, fontName='Helvetica-Bold',
             textColor=colors.white, spaceBefore=14, spaceAfter=6)
intro    = S('Normal', fontSize=10, leading=15, spaceAfter=10,
             alignment=TA_JUSTIFY, textColor=colors.HexColor('#2C3E50'))
bullet0  = S('Normal', fontSize=10, leading=15, leftIndent=16, spaceAfter=5,
             alignment=TA_JUSTIFY)
bullet1  = S('Normal', fontSize=10, leading=15, leftIndent=36, spaceAfter=4,
             alignment=TA_JUSTIFY, textColor=colors.HexColor('#2C3E50'))
scenario = S('Normal', fontSize=10.5, leading=15, fontName='Helvetica-Bold',
             textColor=BLUE_MID, spaceBefore=10, spaceAfter=4)
step_num = S('Normal', fontSize=10, leading=15, fontName='Helvetica-Bold',
             textColor=BLUE_DARK)
footer_s = S('Normal', fontSize=7, leading=9, textColor=colors.grey, alignment=TA_CENTER)
boiler   = S('Normal', fontSize=9, leading=12, textColor=colors.HexColor('#555555'),
             alignment=TA_CENTER)
boiler_h = S('Normal', fontSize=11, leading=14, fontName='Helvetica-Bold',
             textColor=BLUE_DARK, alignment=TA_CENTER)

# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(BLUE_DARK)
    canvas.rect(MARGIN, PAGE_H - MARGIN - 0.7*cm, CONTENT_W, 0.7*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(MARGIN + 4, PAGE_H - MARGIN - 0.5*cm,
                      'Capacitación en Procesamiento de Software LMS')
    canvas.drawRightString(PAGE_W - MARGIN - 4, PAGE_H - MARGIN - 0.5*cm,
                           'Mejores Prácticas para Vuelo de Producción')
    # Footer line
    y_foot = MARGIN - 2*mm
    canvas.setStrokeColor(BLUE_DARK)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, y_foot + 6*mm, PAGE_W - MARGIN, y_foot + 6*mm)
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.grey)
    canvas.drawString(MARGIN, y_foot, 'Teledyne Optech Incorporated')
    canvas.drawRightString(PAGE_W - MARGIN, y_foot, f'Página {doc.page}')
    canvas.restoreState()

# ── Section heading helper ────────────────────────────────────────────────────
def section_block(title):
    tbl = Table([[Paragraph(title, section)]],
                colWidths=[CONTENT_W])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), BLUE_DARK),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('ROUNDEDCORNERS',[4]),
    ]))
    return tbl

def step_row(num, text, sub=False):
    sty   = bullet1 if sub else bullet0
    n_sty = S('Normal', fontSize=10, leading=15, fontName='Helvetica-Bold',
               textColor=BLUE_DARK if not sub else BLUE_MID,
               leftIndent=0)
    col1 = 0.9*cm if not sub else 1.4*cm
    lpad = 0.5*cm if not sub else 1.0*cm
    tbl = Table([[Paragraph(str(num), n_sty), Paragraph(text, sty)]],
                colWidths=[col1, CONTENT_W - col1 - lpad])
    tbl.setStyle(TableStyle([
        ('TOPPADDING',   (0,0),(-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ]))
    return tbl

def bullet(symbol, text, sub=False):
    sty  = bullet1 if sub else bullet0
    col1 = 0.6*cm if not sub else 1.0*cm
    tbl = Table([[Paragraph(symbol, step_num), Paragraph(text, sty)]],
                colWidths=[col1, CONTENT_W - col1])
    tbl.setStyle(TableStyle([
        ('TOPPADDING',   (0,0),(-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    ]))
    return tbl

# ── Build ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT_PDF, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN + 1.2*cm, bottomMargin=MARGIN + 1.2*cm,
)

story = []
def add(x): story.append(x)
def sp(h=0.3): story.append(Spacer(1, h*cm))
def hr(c=GREY_LINE): story.append(HRFlowable(width='100%', thickness=0.5, color=c, spaceAfter=6))

# ── PORTADA ───────────────────────────────────────────────────────────────────
sp(1.5)
# Logo / imagen corporativa
if os.path.exists(LOGO_IMG):
    img = Image(LOGO_IMG)
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(CONTENT_W / iw, 2.5*cm / ih)
    img.drawWidth  = iw * scale
    img.drawHeight = ih * scale
    img.hAlign = 'CENTER'
    add(img)

sp(1.0)

# Título
title_tbl = Table(
    [[Paragraph('Capacitación en Procesamiento de Software LMS',
                S('Normal', fontSize=20, fontName='Helvetica-Bold',
                  textColor=BLUE_DARK, alignment=TA_CENTER))],
     [Paragraph('Mejores Prácticas para Vuelo de Producción',
                S('Normal', fontSize=15, fontName='Helvetica',
                  textColor=BLUE_MID, alignment=TA_CENTER))]],
    colWidths=[CONTENT_W])
title_tbl.setStyle(TableStyle([
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('LINEBELOW',    (0,0),(0,0), 1.5, BLUE_DARK),
    ('LINEBELOW',    (0,1),(0,1), 0.5, BLUE_MID),
]))
add(title_tbl)
sp(2.0)

# Datos corporativos
add(Paragraph('Teledyne Optech Incorporated', boiler_h))
sp(0.2)
add(Paragraph('Tel:  +1 905 660 0808      Fax:  +1 905 660 0829', boiler))
add(Paragraph('Correo electrónico: technical.solutions@teledyneoptech.com', boiler))
sp(1.5)
hr(BLUE_MID)
sp(0.5)

# Introducción
add(Paragraph(
    'Este documento describe las mejores prácticas de procesamiento de datos '
    'al realizar levantamientos de grandes áreas.',
    intro))

sp(0.8)

# ── SECCIÓN 1: Planificación de vuelo ────────────────────────────────────────
add(KeepTogether([
    section_block('1.  Planificación de Vuelo'),
    sp(0.3),
]))
sp(0.3)

steps_s1 = [
    (1, 'Planifique primero el área de producción con sus parámetros óptimos de PRF, '
        'Frecuencia de Barrido, FOV y AGL. Trace una línea de cruce o 2 líneas de cruce '
        'opuestas que atraviesen todas las líneas de producción:'),
    (2, 'Realice un vuelo de calibración (3 × 3 + 1) sobre un área residencial '
        'con los mismos parámetros de vuelo.'),
]
for num, text in steps_s1:
    add(step_row(num, text))
    sp(0.15)

sp(0.5)

# ── SECCIÓN 2: Bloque Boresight en LMS ───────────────────────────────────────
add(KeepTogether([
    section_block('2.  Bloque Boresight en LMS'),
    sp(0.3),
]))
sp(0.3)

steps_s2 = [
    (1, False, 'Procese el vuelo de calibración en LMS con el tipo de bloque '
               '"<b>Boresight + Corrección Polinomial del Sensor</b>".'),
    (2, False, 'Acepte el resultado de calibración y guarde el nuevo archivo LCP '
               'si se cumplen las condiciones siguientes:'),
    (None, True, 'El gráfico de error del plano de amarre (<i>tie plane</i>) en el '
                 'diagrama LMS refinado es una línea delgada (± 5 cm) y recta;'),
    (None, True, 'El error horizontal (RMS de línea de techo) es menor que '
                 '<b>AGL × 1/10 000</b>.'),
    (3, False, 'Repita el Paso 2 un máximo de 2 veces si no se cumplen las condiciones; '
               'si el resultado sigue sin ser satisfactorio, envíe los datos de calibración '
               'a Optech.'),
]
for item in steps_s2:
    num, sub, text = item
    if num is None:
        add(bullet('•', text, sub=True))
    else:
        add(step_row(num, text, sub=False))
    sp(0.15)

sp(0.5)

# ── SECCIÓN 3: Bloque de Producción en LMS ───────────────────────────────────
add(section_block('3.  Bloque de Producción en LMS'))
sp(0.3)

add(Paragraph(
    'Existen <b>2 escenarios diferentes</b> para procesar una gran área de producción.',
    normal))
sp(0.3)

# ── Escenario A: Bloque Único ─────────────────────────────────────────────────
add(Paragraph(
    'Escenario A — Método de Bloque Único (<i>Single-Block</i>)',
    scenario))
add(Paragraph(
    'Aplicable cuando el área completa contiene <b>menos de 4 vuelos</b> y/o el equipo '
    'de procesamiento es muy potente (64+ CPUs y almacenamiento SSD suficiente).',
    S('Normal', fontSize=9.5, leading=14, spaceAfter=6, textColor=colors.HexColor('#555555'),
      leftIndent=8)))
sp(0.2)

steps_A = [
    'Cree un proyecto en LMS y agregue una misión por vuelo; para cada misión, '
    'añada todas las líneas de vuelo como líneas ALS, de modo que el proyecto '
    'tenga <b>17 líneas ALS</b> en total.',
    'Configure las Líneas <b>#16 y #17</b> como "<b>Línea de Cruce</b>" '
    'en lugar de "<b>Línea de Producción</b>".',
    'Cree un bloque y agregue las 17 líneas al mismo.',
    'Seleccione "<b>Production</b>" como tipo de bloque y termine de crearlo.',
    'Expanda los detalles del bloque y corrija las correcciones de '
    '<b>Orientación y Posición</b> para las Líneas #16 y #17.',
    'Ejecute el bloque.',
    'Revise el gráfico del plano de amarre del resultado refinado para verificar '
    'que sea delgado y recto; también revise el desplazamiento horizontal para '
    'confirmar que cumple las especificaciones.',
]
for i, text in enumerate(steps_A, 1):
    add(step_row(i, text))
    sp(0.1)

sp(0.4)

# ── Escenario B: Múltiples Bloques ────────────────────────────────────────────
add(Paragraph(
    'Escenario B — Método de Múltiples Bloques (<i>Multiple-Block</i>)',
    scenario))
add(Paragraph(
    'Aplicable cuando el área completa contiene <b>más de 4 vuelos</b> y/o el equipo '
    'de procesamiento no es suficientemente potente.',
    S('Normal', fontSize=9.5, leading=14, spaceAfter=6, textColor=colors.HexColor('#555555'),
      leftIndent=8)))
sp(0.2)

# Día 1
add(Paragraph('▸  Día 1', S('Normal', fontSize=10, fontName='Helvetica-Bold',
              textColor=BLUE_DARK, spaceBefore=4, spaceAfter=3)))

steps_B1 = [
    (1,  'Cree un proyecto en LMS y agregue los datos del Día 1 como <b>Misión 01</b>.'),
    (2,  'Añada las Líneas 1 a 5, y las Líneas 16 y 17, como líneas ALS.'),
    (3,  'Cree el <b>Bloque 01</b> y seleccione las 7 líneas en él.'),
    (4,  'Seleccione "<b>Production</b>" como tipo de bloque y termine de crearlo.'),
    (5,  'Expanda los detalles del bloque y corrija las correcciones de '
         '<b>Orientación y Posición</b> para las Líneas #16 y #17.'),
    (6,  'Ejecute el bloque.'),
    (7,  'Revise el gráfico del plano de amarre del resultado refinado para verificar '
         'que sea delgado y recto; también revise el desplazamiento horizontal.'),
]
for num, text in steps_B1:
    add(step_row(num, text))
    sp(0.1)

sp(0.3)
add(Paragraph('▸  Día 2', S('Normal', fontSize=10, fontName='Helvetica-Bold',
              textColor=BLUE_DARK, spaceBefore=4, spaceAfter=3)))

steps_B2 = [
    (8,  'Agregue los datos del Día 2 como <b>Misión 02</b>.'),
    (9,  'Añada las Líneas 6 a 10 como líneas ALS.'),
    (10, 'Cree un nuevo <b>Bloque 02</b> y seleccione las Líneas 6 a 10 del Día 2.'),
    (11, 'Seleccione las Líneas <b>#16 y #17</b> como "<b>Líneas de Control</b>": '
         'LMS utilizará los resultados refinados de estas dos líneas de cruce como '
         'puntos de control para restringir los resultados de calibración del Bloque 02.'),
    (12, 'Seleccione "<b>Production</b>" como tipo de bloque y termine de crearlo.'),
    (13, 'Ejecute el bloque y, posteriormente, revise el gráfico del plano de amarre '
         'del resultado refinado para verificar que sea delgado y recto; '
         'también revise el desplazamiento horizontal.'),
]
for num, text in steps_B2:
    add(step_row(num, text))
    sp(0.1)

sp(0.3)
add(Paragraph('▸  Día 3 y días adicionales', S('Normal', fontSize=10, fontName='Helvetica-Bold',
              textColor=BLUE_DARK, spaceBefore=4, spaceAfter=3)))

steps_B3 = [
    (14, 'Repita los Pasos 8 a 13 para el Día 3 (y subsiguientes).'),
    (15, 'Revise las zonas de solapamiento entre los Días 1, 2 y 3. Dado que los '
         '3 bloques comparten las mismas líneas de cruce como control, '
         'las áreas de solapamiento no deberían presentar desalineaciones.'),
]
for num, text in steps_B3:
    add(step_row(num, text))
    sp(0.1)

sp(1.0)
hr(BLUE_MID)
sp(0.4)

# Pie de página corporativo
add(Paragraph(
    '© Teledyne Optech Incorporated — Todos los derechos reservados<br/>'
    'Para más información: <font color="#2980B9">technical.solutions@teledyneoptech.com</font>',
    S('Normal', fontSize=8, leading=12, textColor=colors.grey, alignment=TA_CENTER)))

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF generado: {OUT_PDF}')
