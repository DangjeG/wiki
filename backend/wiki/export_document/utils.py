from io import BytesIO

from docx import Document as Doc
from spire.doc import Document, FileFormat, XHTMLValidationType, Stream


async def convert(data: str) -> BytesIO:
    document = Document()

    stream = Stream(data.encode(encoding='UTF-8'))

    document.LoadFromStream(stream, FileFormat.Html, XHTMLValidationType.none)

    result_stream = Stream()

    document.SaveToStream(result_stream)

    array_bytes = result_stream.ToArray()

    result_bytes = b''.join(array_bytes)

    document.Close()

    result_bytes = await remove_watermark(Doc(BytesIO(result_bytes)))

    return result_bytes


async def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    paragraph._p = paragraph._element = None


async def remove_watermark(doc: Doc):
    i = 0
    while i < len(doc.paragraphs):
        if 'Evaluation Warning: The document was created with Spire.Doc for Python.' in doc.paragraphs[i].text:
            for j in range(1):
                await delete_paragraph(doc.paragraphs[j])
        i += 1
    result_bytes = BytesIO()

    doc.save(result_bytes)

    return result_bytes


async def export_document(file_name: str, list_document_content: list[str]):
    html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
         <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <title></title>
         </head>
         <body>"""

    for content in list_document_content:
        html += content

    html += """</body>
        </html>"""

    return await convert(html)
