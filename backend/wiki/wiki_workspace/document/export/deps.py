from dataclasses import dataclass

from wiki.wiki_workspace.document.export.converter.docx import HtmlToDocxConverter
from wiki.wiki_workspace.document.export.converter.pdf import HtmlToPdfConverter


@dataclass
class DocumentConverters:
    pdf: HtmlToPdfConverter
    docx: HtmlToDocxConverter


def get_converters():
    yield DocumentConverters(
        pdf=HtmlToPdfConverter(),
        docx=HtmlToDocxConverter()
    )
