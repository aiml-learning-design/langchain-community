"""
UniversalDocumentLoader

This Document loader supports the following file extensions and their respective MIME types:

- .pdf    → application/pdf (Portable Document Format)
- .txt    → text/plain (Plain Text)
- .docx   → application/vnd.openxmlformats-officedocument.wordprocessingml.document (Microsoft Word Document)
- .pptx   → application/vnd.openxmlformats-officedocument.presentationml.presentation (Microsoft PowerPoint)
- .rtf    → application/rtf (Rich Text Format)
- .eml    → message/rfc822 (Email Message)
- .msg    → application/vnd.ms-outlook (Outlook Message)
- .csv    → text/csv (Comma Separated Values)
- .html   → text/html (HTML Documents)
- .htm    → text/html (HTML Documents)
- .md     → text/markdown (Markdown)
- .json   → (not implemented, extend by registering a handler)

To add support for more types like `.epub`, `.xlsx`, or `.json`, extend using `add_handler(mimetype, parser)`.
"""

from typing import List, Optional, Dict, Any
from langchain_core.documents import Document

from libs.community.langchain_community.universal_document_loader.universal_document_loader_base import UniversalDocumentLoaderBase
from libs.community.langchain_community.document_loaders.parsers.generic import MimeTypeBasedParser
from libs.community.langchain_community.document_loaders.blob_loaders.file_system import FileSystemBlobLoader

# Parsers
from libs.community.langchain_community.document_loaders.parsers.html.bs4 import BS4HTMLParser
from libs.community.langchain_community.document_loaders.parsers.pdf import PDFMinerParser
from libs.community.langchain_community.document_loaders.parsers.txt import TextParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_rtf import RTFParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_csv import CSVParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_docx import DocxParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_email import EmailParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_markdown import MarkdownParser
from libs.community.langchain_community.universal_document_loader.custom_parsers.parser_ppt import PowerPointParser


class UniversalDocumentLoader(UniversalDocumentLoaderBase):
    """
    A universal document loader that intelligently chooses the appropriate parser
    based on MIME type, and supports fallback parsing when the type is unknown.

    Usage:
        loader = UniversalDocumentLoader("path/to/file.docx")
        docs = loader.load()

    Supports dynamic extension by registering custom handlers:
        loader.add_handler("application/json", CustomJsonParser())

    Parameters:
    - file_path (str): Path to the file to be loaded.
    - fallback_parser (Optional[Any]): Parser to use when MIME type is unknown.
    """

    def __init__(self, file_path: str, fallback_parser: Optional[Any] = None):
        super().__init__(file_path, fallback_parser)
        self.handlers = self._get_default_handlers()
        if self.fallback_parser is None:
            self.fallback_parser = TextParser()
        self.parser = MimeTypeBasedParser(handlers=self.handlers, fallback_parser=self.fallback_parser)

    def load(self) -> List[Document]:
        """Load and parse the document using the appropriate MIME-based parser."""
        blob_loader = FileSystemBlobLoader(self.file_path)
        blobs = list(blob_loader.yield_blobs())
        if not blobs:
            raise ValueError(f"No blobs found at: {self.file_path}")
        return list(self.parser.lazy_parse(blobs[0]))

    def add_handler(self, mimetype: str, handler: Any):
        """
        Register or override a handler for a specific MIME type.

        Args:
            mimetype (str): The MIME type to handle (e.g., 'application/json').
            handler (Any): A parser instance that implements `.lazy_parse(blob)`.
        """
        self.handlers[mimetype] = handler
        self.parser = MimeTypeBasedParser(handlers=self.handlers, fallback_parser=self.fallback_parser)

    def _get_default_handlers(self) -> Dict[str, Any]:
        """
        Returns the default MIME type to parser mapping.

        Extend this method or use `add_handler` for custom parsers.
        """
        return {
            "application/pdf": PDFMinerParser(),
            "text/plain": TextParser(),
            "text/csv": CSVParser(),
            "application/rtf": RTFParser(),
            "text/markdown": MarkdownParser(),
            "application/vnd.ms-outlook": EmailParser(),
            "message/rfc822": EmailParser(),
            "text/html": BS4HTMLParser(),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxParser(),
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": PowerPointParser(),
        }