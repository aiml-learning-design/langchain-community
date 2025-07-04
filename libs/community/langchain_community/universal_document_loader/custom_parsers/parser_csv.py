import pandas as pd
from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.blob_loaders.schema import Blob
from langchain_core.documents import Document
from typing import List


class CSVParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> List[Document]:
        """Parse CSV file into a Document.

        Args:
            blob: Blob object containing the CSV file path

        Returns:
            List[Document]: A list containing a single Document with the CSV content
        """
        df = pd.read_csv(blob.path)
        return [Document(page_content=df.to_csv(index=False), metadata={"source": str(blob.path)})]