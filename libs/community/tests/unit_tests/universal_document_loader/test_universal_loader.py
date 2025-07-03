import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document

from libs.community.langchain_community.universal_document_loader.universal_loader import UniversalDocumentLoader

# Mapping to patch correct internal loader import location
LOADER_CLASS_MODULE = "libs.community.langchain_community.universal_document_loader.universal_loader"


@pytest.mark.parametrize(
    "file_path,expected_loader_class",
    [
        ("sample_documents/sample.pdf", "UnstructuredPDFLoader"),
        ("sample_documents/sample.docx", "UnstructuredWordDocumentLoader"),
        ("sample_documents/sample.rtf", "UnstructuredRTFLoader"),
        ("sample_documents/sample.html", "UnstructuredHTMLLoader"),
        ("sample_documents/sample.eml", "UnstructuredEmailLoader"),
        ("sample_documents/sample.msg", "UnstructuredEmailLoader"),
        ("sample_documents/sample.md", "UnstructuredMarkdownLoader"),
        ("sample_documents/sample.pptx", "UnstructuredPowerPointLoader"),
        ("sample_documents/sample.txt", "TextLoader"),
        ("sample_documents/sample.csv", "CSVLoader"),
        ("sample_documents/sample.unknown", "UnstructuredLoader"),
    ]
)
@patch("os.path.isfile", return_value=True)
def test_loader_strategy_selection(mock_isfile, file_path, expected_loader_class):
    """
    Tests that the correct strategy is used for each file type by verifying
    that the expected loader class is called.
    """
    with patch(f"{LOADER_CLASS_MODULE}.{expected_loader_class}") as MockLoader:
        mock_instance = MagicMock()
        mock_instance.load.return_value = [Document(page_content="Mock content")]
        MockLoader.return_value = mock_instance

        loader = UniversalDocumentLoader(file_path)
        docs = loader.load()

        assert isinstance(docs, list)
        assert isinstance(docs[0], Document)
        MockLoader.assert_called_once_with(file_path)
