import pandas as pd
from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.blob_loaders.schema import Blob
from langchain_core.documents import Document
from typing import List


class CSVParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> List[Document]:
        """"""
        df = pd.read_csv(blob.path)
        return [Document(page_content=df.to_csv(index=False), metadata={"source": str(blob.path)})]
