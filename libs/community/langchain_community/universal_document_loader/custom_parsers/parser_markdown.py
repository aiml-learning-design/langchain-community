from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.blob_loaders.schema import Blob
from langchain_core.documents import Document
from typing import List
import markdown  # Correct import for Python markdown library


class MarkdownParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> List[Document]:
        try:
            with open(blob.path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
                html = markdown.markdown(markdown_content)
                return [Document(page_content=html, metadata={"source": blob.path})]
        except Exception as e:
            return []
