import os
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document


class UniversalDocumentLoaderBase(ABC):
    """
    Abstract base class for a universal document loader.

    This interface defines the contract for any document loader that supports loading
    and parsing documents based on MIME types, with an optional fallback parser.

    Subclasses must implement the `load` and `add_handler` methods.

    Attributes:
        file_path (str): Absolute or relative path to the document file.
        fallback_parser (Optional[Any]): Optional parser to use if no MIME type match is found.
    """

    def __init__(self, file_path: str, fallback_parser: Optional[Any] = None):
        """
        Initialize the universal document loader base.

        Args:
            file_path (str): Path to the document file.
            fallback_parser (Optional[Any]): Parser to use if MIME type is unsupported.
        """
        self.file_path = file_path
        self._validate_file()
        self.fallback_parser = fallback_parser

    def _validate_file(self):
        """
        Validate that the file exists at the given path.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File does not exist: {self.file_path}")

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load and parse the document at the specified path.

        Returns:
            List[Document]: A list of parsed LangChain `Document` objects.
        """
        pass

    @abstractmethod
    def add_handler(self, mimetype: str, handler: Any):
        """
        Register or override a MIME type handler for parsing specific document formats.

        Args:
            mimetype (str): The MIME type string (e.g., 'application/pdf').
            handler (Any): An instance of a parser that implements `lazy_parse(blob)`.
        """
        pass