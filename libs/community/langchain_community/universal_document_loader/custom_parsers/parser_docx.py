from typing import Iterator

from langchain_core.document_loaders import BaseBlobParser
from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from libs.community.langchain_community.document_loaders.word_document import Docx2txtLoader


class DocxParser(BaseBlobParser):
    """
    Blob-compatible parser that wraps `Docx2txtLoader` to work with `MimeTypeBasedParser`.


    Args:
        blob: Blob object containing the CSV file path

    Returns:
        List[Document]: A list containing a single Document with the DOCX content

    """

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        loader = Docx2txtLoader(blob.path)
        for doc in loader.load():
            yield doc
