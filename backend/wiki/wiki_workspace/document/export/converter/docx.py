from io import BytesIO

from html2docx import HTML2Docx

from wiki.wiki_workspace.document.export.converter.base import BaseConverter


class HtmlToDocxConverter(BaseConverter):

    def convert(self, source: str | bytes | BytesIO) -> bytes:
        parser = HTML2Docx("Document")
        parser.feed(source.strip())

        buf = BytesIO()
        parser.doc.save(buf)

        return buf.getvalue()
