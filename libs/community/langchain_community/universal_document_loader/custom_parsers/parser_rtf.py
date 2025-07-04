from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.rtf import UnstructuredRTFLoader
from langchain_community.document_loaders.blob_loaders.schema import Blob


class RTFParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob):
        loader = UnstructuredRTFLoader(file_path=blob.path)
        for doc in loader.load():
            yield doc
