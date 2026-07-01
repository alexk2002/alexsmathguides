# -*- coding: utf-8 -*-
"""Generiert die kostenlosen Abitur-PDFs fuer alexsmathguides."""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

INDIGO_DARK = colors.HexColor("#1A237E")
INDIGO_LIGHT = colors.HexColor("#E8EAF6")
TEXT_DARK = colors.HexColor("#212121")
MUTED = colors.HexColor("#5C6BC0")

PDFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
os.makedirs(PDFS_DIR, exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=28, textColor=colors.white, alignment=TA_LEFT, spaceAfter=4,
)
subtitle_style = ParagraphStyle(
    "SubtitleStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=12, textColor=colors.white, alignment=TA_LEFT,
)
section_style = ParagraphStyle(
    "SectionStyle", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=15, textColor=INDIGO_DARK, spaceBefore=18, spaceAfter=8,
    borderPadding=0,
)
box_title_style = ParagraphStyle(
    "BoxTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=12, textColor=INDIGO_DARK, spaceAfter=3,
)
box_formula_style = ParagraphStyle(
    "BoxFormula", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11.5, textColor=TEXT_DARK, spaceAfter=3,
)
box_body_style = ParagraphStyle(
    "BoxBody", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=TEXT_DARK, leading=14,
)
body_style = ParagraphStyle(
    "BodyStyle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10.5, textColor=TEXT_DARK, leading=15,
)
bullet_style = ParagraphStyle(
    "BulletStyle", parent=body_style, leftIndent=12, spaceAfter=4,
)
table_header_style = ParagraphStyle(
    "TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10, textColor=colors.white, alignment=TA_CENTER,
)
table_cell_style = ParagraphStyle(
    "TableCell", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=TEXT_DARK, alignment=TA_CENTER,
)


def header_flowable(title, subtitle):
    tbl = Table(
        [[Paragraph(title, title_style)], [Paragraph(subtitle, subtitle_style)]],
        colWidths=[170 * mm],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INDIGO_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
        ("TOPPADDING", (0, 1), (-1, 1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ]))
    return tbl


def rule_box(name, formula, example):
    data = [
        [Paragraph(name, box_title_style)],
        [Paragraph(formula, box_formula_style)],
        [Paragraph(example, box_body_style)],
    ]
    tbl = Table(data, colWidths=[170 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INDIGO_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.75, INDIGO_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("TOPPADDING", (0, 1), (-1, 2), 2),
        ("BOTTOMPADDING", (0, 0), (-1, 1), 2),
    ]))
    return KeepTogether(tbl)


def section_title(text):
    return Paragraph(text, section_style)


def hr():
    return HRFlowable(width="100%", thickness=0.75, color=INDIGO_LIGHT, spaceBefore=2, spaceAfter=10)


def bullets(items):
    flow = []
    for i, item in enumerate(items, start=1):
        flow.append(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{item}", bullet_style))
    return flow


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(
        A4[0] / 2, 12 * mm, f"alexsmathguides · Seite {doc.page}"
    )
    canvas.setStrokeColor(INDIGO_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, 16 * mm, A4[0] - 20 * mm, 16 * mm)
    canvas.restoreState()


def build_doc(filename):
    return SimpleDocTemplate(
        os.path.join(PDFS_DIR, filename),
        pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=14 * mm, bottomMargin=20 * mm,
        title=filename,
    )


# ---------------------------------------------------------------------------
# PDF 1: Ableitungsregeln
# ---------------------------------------------------------------------------

def build_ableitungsregeln():
    doc = build_doc("ableitungsregeln.pdf")
    story = []

    story.append(header_flowable("Ableitungsregeln", "Übersicht für die Oberstufe & das Abitur"))
    story.append(Spacer(1, 14))

    story.append(section_title("Grundidee der Ableitung"))
    story.append(hr())
    story.append(Paragraph(
        "Die Ableitung f'(x) einer Funktion f(x) beschreibt die <b>momentane "
        "Änderungsrate</b> an einer Stelle x – also wie stark sich der Funktionswert "
        "gerade ändert. Geometrisch entspricht f'(x) der <b>Steigung der Tangente</b> "
        "an den Funktionsgraphen im Punkt (x | f(x)).",
        body_style,
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Formal ist die Ableitung der Grenzwert des Differenzenquotienten: "
        "f'(x) = lim<sub>h→0</sub> [f(x+h) − f(x)] / h. In der Praxis nutzt man "
        "jedoch fast immer die folgenden Ableitungsregeln, um schnell und sicher "
        "abzuleiten.",
        body_style,
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Die wichtigsten Ableitungsregeln"))
    story.append(hr())

    rules = [
        ("Konstantenregel",
         "f(x) = c  ⟹  f'(x) = 0",
         "Beispiel: f(x) = 7  ⟹  f'(x) = 0 (eine Konstante hat keine Steigung)."),
        ("Faktorregel",
         "f(x) = c · g(x)  ⟹  f'(x) = c · g'(x)",
         "Beispiel: f(x) = 5x³  ⟹  f'(x) = 5 · 3x² = 15x²."),
        ("Summenregel",
         "f(x) = g(x) + h(x)  ⟹  f'(x) = g'(x) + h'(x)",
         "Beispiel: f(x) = x² + 3x  ⟹  f'(x) = 2x + 3."),
        ("Differenzregel",
         "f(x) = g(x) − h(x)  ⟹  f'(x) = g'(x) − h'(x)",
         "Beispiel: f(x) = x³ − 4x  ⟹  f'(x) = 3x² − 4."),
        ("Potenzregel",
         "f(x) = xⁿ  ⟹  f'(x) = n · xⁿ⁻¹",
         "Beispiel: f(x) = x⁴  ⟹  f'(x) = 4x³. Auch für Wurzeln: f(x) = √x = x^(1/2) "
         "⟹ f'(x) = ½ · x⁻¹ᐟ² = 1/(2√x)."),
        ("Produktregel",
         "f(x) = u(x) · v(x)  ⟹  f'(x) = u'(x) · v(x) + u(x) · v'(x)",
         "Beispiel: f(x) = x² · sin(x)  ⟹  f'(x) = 2x · sin(x) + x² · cos(x)."),
        ("Quotientenregel",
         "f(x) = u(x) / v(x)  ⟹  f'(x) = [u'(x) · v(x) − u(x) · v'(x)] / v(x)²",
         "Beispiel: f(x) = x / (x+1)  ⟹  f'(x) = [1·(x+1) − x·1] / (x+1)² = 1/(x+1)²."),
        ("Kettenregel",
         "f(x) = u(v(x))  ⟹  f'(x) = u'(v(x)) · v'(x)  (äußere · innere Ableitung)",
         "Beispiel: f(x) = (3x + 2)⁵  ⟹  f'(x) = 5·(3x+2)⁴ · 3 = 15·(3x+2)⁴."),
    ]

    for name, formula, example in rules:
        story.append(rule_box(name, formula, example))
        story.append(Spacer(1, 8))

    story.append(section_title("Tabelle der Standardableitungen"))
    story.append(hr())

    table_data = [
        [Paragraph("f(x)", table_header_style), Paragraph("f'(x)", table_header_style)],
        ["xⁿ", "n · xⁿ⁻¹"],
        ["eˣ", "eˣ"],
        ["aˣ", "aˣ · ln(a)"],
        ["ln(x)", "1/x"],
        ["sin(x)", "cos(x)"],
        ["cos(x)", "−sin(x)"],
        ["tan(x)", "1/cos²(x)"],
        ["√x", "1/(2√x)"],
        ["1/x", "−1/x²"],
    ]
    table_data_p = [table_data[0]] + [
        [Paragraph(a, table_cell_style), Paragraph(b, table_cell_style)]
        for a, b in table_data[1:]
    ]
    std_table = Table(table_data_p, colWidths=[85 * mm, 85 * mm])
    std_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO_DARK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, INDIGO_LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, INDIGO_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(std_table)
    story.append(Spacer(1, 12))

    story.append(section_title("Typische Fehler"))
    story.append(hr())
    story.extend(bullets([
        "Potenzregel bei Summen falsch anwenden – jeder Summand wird einzeln abgeleitet, "
        "nicht die ganze Klammer als Potenz behandelt.",
        "Die Kettenregel vergessen: bei verketteten Funktionen (z. B. (2x+1)³) muss die "
        "innere Ableitung mit multipliziert werden.",
        "Vorzeichenfehler bei der Ableitung von cos(x): die Ableitung ist −sin(x), nicht sin(x).",
        "Produktregel und Quotientenregel verwechseln oder eine Seite vergessen "
        "(z. B. nur u'(x)·v(x) statt der vollständigen Summe).",
        "Konstanten wie 'c' fälschlich mit ableiten, obwohl sie beim Ableiten einfach "
        "verschwinden (Konstantenregel).",
    ]))
    story.append(Spacer(1, 12))

    story.append(section_title("Mini-Strategie zum Ableiten"))
    story.append(hr())
    story.extend(bullets([
        "Funktion genau anschauen: Summe, Produkt, Quotient oder Verkettung erkennen.",
        "Passende Regel(n) auswählen (ggf. mehrere Regeln kombinieren).",
        "Innere und äußere Funktion bei Verkettungen klar trennen.",
        "Schritt für Schritt ableiten und Zwischenergebnisse notieren.",
        "Ergebnis vereinfachen und auf Vorzeichen- sowie Rechenfehler prüfen.",
    ]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


# ---------------------------------------------------------------------------
# PDF 2: Stochastik-Formelsammlung
# ---------------------------------------------------------------------------

def build_stochastik():
    doc = build_doc("stochastik_formelsammlung.pdf")
    story = []

    story.append(header_flowable("Stochastik-Formelsammlung", "Die wichtigsten Formeln für die Oberstufe & das Abitur"))
    story.append(Spacer(1, 14))

    story.append(section_title("Grundbegriffe"))
    story.append(hr())
    story.append(rule_box(
        "Ergebnismenge Ω und Ereignis",
        "Ω = Menge aller möglichen Ergebnisse, Ereignis A ⊆ Ω",
        "Beispiel: Beim Würfeln ist Ω = {1,2,3,4,5,6}. Das Ereignis A = \"gerade Zahl\" "
        "ist A = {2,4,6}."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Gegenereignis",
        "P(Ā) = 1 − P(A)",
        "Beispiel: P(\"mindestens einmal Kopf\" bei 3 Würfen) = 1 − P(\"nie Kopf\")."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Sichere & unmögliche Ereignisse",
        "P(∅) = 0  und  P(Ω) = 1",
        "Das unmögliche Ereignis ∅ hat Wahrscheinlichkeit 0, das sichere Ereignis Ω "
        "hat Wahrscheinlichkeit 1."
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Pfadregeln & Mengenregeln"))
    story.append(hr())
    story.append(rule_box(
        "Additionssatz (Vereinigung)",
        "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)",
        "Beispiel: P(\"Zahl gerade oder durch 3 teilbar\") = P(gerade) + P(durch 3) "
        "− P(gerade UND durch 3)."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Multiplikationsregel (Pfadmultiplikation)",
        "P(A ∩ B) = P(A) · P(B|A)   (\"Punkt vor Strich\" im Baumdiagramm)",
        "Beispiel: Ziehen ohne Zurücklegen – die Wahrscheinlichkeit eines Pfades im "
        "Baumdiagramm ergibt sich durch Multiplikation der Äste."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Summenregel (Pfadaddition)",
        "P(Ereignis) = Summe aller passenden Pfadwahrscheinlichkeiten",
        "Beispiel: Führen mehrere Pfade im Baumdiagramm zum gesuchten Ereignis, werden "
        "ihre Wahrscheinlichkeiten addiert."
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Bedingte Wahrscheinlichkeit"))
    story.append(hr())
    story.append(rule_box(
        "Bedingte Wahrscheinlichkeit",
        "P(A|B) = P(A ∩ B) / P(B),  mit P(B) > 0",
        "Beispiel: P(\"Fehler erkannt\" | \"Bauteil ist defekt\") beschreibt die "
        "Wahrscheinlichkeit von A, wenn B bereits eingetreten ist."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Stochastische Unabhängigkeit",
        "A und B unabhängig  ⟺  P(A ∩ B) = P(A) · P(B)  ⟺  P(A|B) = P(A)",
        "Beispiel: Zwei unabhängige Münzwürfe – das Ergebnis des ersten Wurfs "
        "beeinflusst die Wahrscheinlichkeit des zweiten nicht."
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Binomialverteilung"))
    story.append(hr())
    story.append(rule_box(
        "Einzelwahrscheinlichkeit",
        "P(X = k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ",
        "n = Anzahl der Versuche, k = Anzahl der Erfolge, p = Erfolgswahrscheinlichkeit. "
        "Beispiel: n = 10 Würfe, p = 1/6, P(X = 2) = C(10,2) · (1/6)² · (5/6)⁸."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Erwartungswert, Varianz & Standardabweichung",
        "E(X) = μ = n · p    Var(X) = σ² = n · p · (1−p)    σ = √(n · p · (1−p))",
        "Beispiel: n = 200, p = 0,3  ⟹  μ = 60, σ² = 42, σ = √42 ≈ 6,48."
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Kombinatorik"))
    story.append(hr())
    story.append(rule_box(
        "Fakultät",
        "n! = n · (n−1) · (n−2) · … · 2 · 1,   0! = 1",
        "Beispiel: 5! = 5 · 4 · 3 · 2 · 1 = 120."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Binomialkoeffizient",
        "C(n,k) = n! / [k! · (n−k)!]",
        "Beispiel: C(6,2) = 6! / (2! · 4!) = 15 – Anzahl der Möglichkeiten, aus 6 "
        "Elementen 2 auszuwählen."
    ))
    story.append(Spacer(1, 10))

    story.append(section_title("Hypothesentests"))
    story.append(hr())
    story.append(rule_box(
        "Nullhypothese & Gegenhypothese",
        "H₀: Annahme, die getestet wird     H₁: Gegenhypothese",
        "Beispiel: H₀: \"Der Anteil ist p = 0,5\", H₁: \"Der Anteil ist p ≠ 0,5\"."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Signifikanzniveau α",
        "α = maximale Wahrscheinlichkeit für einen Fehler 1. Art",
        "Typische Werte: α = 0,05 (5 %) oder α = 0,01 (1 %)."
    ))
    story.append(Spacer(1, 8))
    story.append(rule_box(
        "Annahme- und Ablehnungsbereich",
        "Ablehnungsbereich: Werte von X, bei denen H₀ verworfen wird",
        "Beispiel: Bei einem rechtsseitigen Test wird H₀ abgelehnt, wenn X ≥ k mit "
        "P(X ≥ k) ≤ α ist."
    ))
    story.append(Spacer(1, 12))

    story.append(section_title("Typische Aufgabenformen"))
    story.append(hr())
    story.extend(bullets([
        "Baumdiagramme erstellen und mit Pfadregeln kombinierte Wahrscheinlichkeiten "
        "berechnen.",
        "Kenngrößen der Binomialverteilung (μ, σ, σ²) bestimmen und interpretieren.",
        "Bedingte Wahrscheinlichkeiten aus Sachtexten oder Vierfeldertafeln berechnen.",
        "Hypothesentests durchführen: Entscheidungsregel aufstellen, Testgröße "
        "berechnen und Entscheidung begründen.",
    ]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_ableitungsregeln()
    build_stochastik()
    print("PDFs erstellt in:", PDFS_DIR)
