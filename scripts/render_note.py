"""Render the two-page Markdown note using reportlab (authoring tool only)."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="NoteBody", fontName="Helvetica", fontSize=9.4, leading=12.3,
    spaceAfter=7, alignment=TA_LEFT, textColor=colors.HexColor("#223044"),
))
styles["Heading1"].fontSize = 17
styles["Heading1"].leading = 21
styles["Heading1"].textColor = colors.HexColor("#123C58")
styles["Heading2"].fontSize = 11.5
styles["Heading2"].leading = 15


def markup(text):
    return re.sub(
        r"\[([^\]]+)\]\((https://[^)]+)\)",
        r'<link href="\2" color="#12648C">\1</link>', escape(text),
    )


story = []
for block in (ROOT / "docs/REPORT.md").read_text(encoding="utf-8").split("\n\n"):
    block = block.strip()
    if not block:
        continue
    if block == "<!-- pagebreak -->":
        story.append(PageBreak())
    elif block.startswith("# "):
        story.append(Paragraph(markup(block[2:]), styles["Heading1"]))
    elif block.startswith("## "):
        story.append(Paragraph(markup(block[3:]), styles["Heading2"]))
    elif block.startswith("- "):
        for line in block.splitlines():
            story.append(Paragraph(markup(line[2:]), styles["NoteBody"], bulletText="-"))
    else:
        story.append(Paragraph(markup(block.replace("\n", " ")), styles["NoteBody"]))
story.append(Spacer(1, 3))
output = ROOT / "output/pdf/soup-release-note.pdf"
output.parent.mkdir(parents=True, exist_ok=True)


def footer(canvas, document):
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#697587"))
    canvas.drawString(38, 24, "Soup | Release engineering evidence | 2026-11-10")
    canvas.drawRightString(A4[0] - 38, 24, str(document.page))


SimpleDocTemplate(
    str(output), pagesize=A4, rightMargin=38, leftMargin=38,
    topMargin=30, bottomMargin=38, title="Soup release engineering note",
    author="AI-assisted draft for candidate review",
).build(story, onFirstPage=footer, onLaterPages=footer)
print(output)
