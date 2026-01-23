from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os

alignment_map = {
    "left": WD_PARAGRAPH_ALIGNMENT.LEFT,
    "center": WD_PARAGRAPH_ALIGNMENT.CENTER,
    "right": WD_PARAGRAPH_ALIGNMENT.RIGHT,
    "justify": WD_PARAGRAPH_ALIGNMENT.JUSTIFY
}

filePath = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(filePath, "dataDir")

def render(resume):
    '''for section in yaml_file:
        self.doc.add_heading(section, level=1)
        for item in section:
            self.doc.add_paragraph(item, style="Normal")'''

    doc = Document()
    _defined_font = "Arial"

    style1 = doc.styles.add_style("Style14", 1)  # 1 = paragraph style
    style1.font.name = _defined_font
    style1.font.size = Pt(14)
    style2 = doc.styles.add_style("Style12", 1)  # 1 = paragraph style
    style2.font.name = _defined_font
    style2.font.size = Pt(12)
    style3 = doc.styles.add_style("Style10.5", 1)  # 1 = paragraph style
    style3.font.name = _defined_font
    style3.font.size = Pt(10.5)

    name_section = doc.add_paragraph(style="Style14")
    name_section.add_run(resume['contact_section']['name']).bold = True
    name_section.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    contact_section = doc.add_paragraph(style="Style12")
    contact_section.add_run(resume['contact_section']['contact']['phone']).bold = False
    contact_section.add_run(" | ")
    contact_section.add_run(resume['contact_section']['contact']['email']).bold = False
    contact_section.add_run(" | ")
    contact_section.add_run(resume['contact_section']['contact']['linkedin']).bold = False
    contact_section.add_run(" | ")
    contact_section.add_run(resume['contact_section']['contact']['portfolio']).bold = False
    contact_section.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    location_section = doc.add_paragraph(style="Style12")
    location_section.add_run(resume['contact_section']['location']['city']).bold = False
    location_section.add_run(" | ")
    location_section.add_run(resume['contact_section']['location']['state']).bold = False
    location_section.add_run(" | ")
    location_section.add_run(resume['contact_section']['location']['immigration_status']).bold = False
    location_section.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    if resume['summary']['include'] == True:
        summary_section = doc.add_paragraph(style="Style10.5")
        summary_section.add_run(resume['summary']['reason']).bold = True
        summary_section.add_run(" | ")
        summary_section.add_run(resume['summary']['text']).bold = False
    summary_section.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    education_title = doc.add_paragraph(style="Style10.5") # if type 1 nad 2 , else only 1 or only 2
    education_title.add_run("Education & Certificates").bold = True
    for item in resume['education_certificates']['items']:
        education_section = doc.add_paragraph(style="List Bullet")
        if item['type'] == "education":
            education_section.add_run(item['degree']).bold = False
            education_section.add_run(" in ")
            education_section.add_run(item['major']).bold = False
            education_section.add_run(" from ")
            education_section.add_run(item['institution']).bold = False
            education_section.add_run(" | ")
            #if item['graduation_date'] < time 3 year:
            education_section.add_run(item['graduation_date']).bold = False
        if item['type'] == "certificate":
            education_section.add_run(item['name']).bold = False

    doc.save('output.docx')