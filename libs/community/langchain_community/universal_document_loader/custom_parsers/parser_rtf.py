from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.rtf import UnstructuredRTFLoader
from langchain_community.document_loaders.blob_loaders.schema import Blob
from typing import Iterator
from langchain_core.documents import Document


class RTFParser(BaseBlobParser):
    """
    Parser for RTF (Rich Text Format) documents.

    Utilizes `UnstructuredRTFLoader` to extract content from `.rtf` files and yields LangChain-compatible `Document` objects.
    """

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Lazily parses an RTF file from the given blob and yields `Document` objects.

        Args:
            blob (Blob): A blob instance pointing to an `.rtf` file.

        Yields:
            Document: Parsed document content with metadata.
        """
        loader = UnstructuredRTFLoader(file_path=blob.path)
        for doc in loader.load():
            yield doc