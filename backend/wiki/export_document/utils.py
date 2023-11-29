from uuid import UUID

import docx
import spire
from spire.doc import *

def convert3(input_file, output_file):
    document = spire.doc.Document()

    document.LoadFromFile(input_file, FileFormat.Html, XHTMLValidationType.none)

    document.SaveToFile(output_file, FileFormat.Docx2016)
    document.Close()

    remove_watermark(docx.Document("Output3.docx"))


def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    paragraph._p = paragraph._element = None


def remove_watermark(doc):
    i = 0
    while i < len(doc.paragraphs):
        if 'Evaluation Warning: The document was created with Spire.Doc for Python.' in doc.paragraphs[i].text:
            for j in range(1):
                delete_paragraph(doc.paragraphs[j])
        i += 1
    doc.save('Output3.docx')


async def export_document(user_id: UUID, document_id: UUID, list_document_content: list[str]):
    html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Пример веб-страницы</title>
 </head>
 <body>"""
