from io import BytesIO

from xhtml2pdf import pisa

from wiki.wiki_workspace.document.export.converter.base import BaseConverter


class HtmlToPdfConverter(BaseConverter):

    def convert(self, source: str | bytes | BytesIO) -> bytes:
        pdf_data = BytesIO()

        # pisa.CreatePDF(source, dest=pdf_data, encoding="UTF-8")
        pisa.pisaDocument(source, dest=pdf_data, encoding="UTF-8")

        pdf_data.seek(0)
        pdf_bytes = pdf_data.read()
        pdf_data.close()

        return pdf_bytes
