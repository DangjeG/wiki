from io import BytesIO
from html2docx import HTML2Docx


def convert_html_to_docx(data: str, title: str):
    parser = HTML2Docx(title)
    parser.feed(data.strip())

    buf = BytesIO()
    parser.doc.save(buf)

    return buf.getvalue()  # .decode(encoding="ISO-8859-1")


def export_document_docx(content: list[str], title: str):
    html = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
         <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <title>{title}</title>
         </head>
         <body>"""

    for content in content:
        html += content

    html += """</body>
        </html>"""

    return convert_html_to_docx(html, title)
