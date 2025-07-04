from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.blob_loaders.schema import Blob
from langchain_core.documents import Document
from typing import List
import markdown


class MarkdownParser(BaseBlobParser):
    """
    Parser for Markdown (.md) files.

    This parser reads the markdown content from the blob's file path,
    converts it to HTML using the Python `markdown` library,
    and wraps the result in a LangChain `Document` object.
    """

    def lazy_parse(self, blob: Blob) -> List[Document]:
        """
        Lazily parses a Markdown file and returns a list of LangChain Documents.

        Args:
            blob (Blob): A blob object that includes the file path to a `.md` file.

        Returns:
            List[Document]: A list containing a single `Document` with HTML content
                            converted from markdown and basic metadata.
                            Returns an empty list if parsing fails.
        """
        try:
            with open(blob.path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
                html = markdown.markdown(markdown_content)
                return [Document(page_content=html, metadata={"source": blob.path})]
        except Exception as e:
            # In production, consider logging this error
            return []