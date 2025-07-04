import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document

from libs.community.langchain_community.universal_document_loader.universal_loader import UniversalDocumentLoader


@pytest.mark.parametrize(
    "file_path, expected_mime",
    [
        ("sample_documents/sample.txt", "text/plain"),
        ("sample_documents/sample.csv", "text/csv"),
        ("sample_documents/sample.rtf", "application/rtf"),
        ("sample_documents/sample.md", "text/markdown"),
        ("sample_documents/sample.msg", "application/vnd.ms-outlook"),
        ("sample_documents/sample.html", "text/html"),
        ("sample_documents/sample.eml", "message/rfc822"),
        ("sample_documents/sample.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("sample_documents/sample.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
        ("sample_documents/sample.pdf", "application/pdf"),
        ("sample_documents/sample.unknown", None),
    ]
)
@patch("os.path.isfile", return_value=True)
@patch("mimetypes.guess_type")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.UniversalDocumentLoader._get_default_handlers")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.PowerPointParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.DocxParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.EmailParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.MarkdownParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.RTFParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.CSVParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.TextParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.PDFMinerParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.BS4HTMLParser")
@patch("libs.community.langchain_community.universal_document_loader.universal_loader.FileSystemBlobLoader")
def test_universal_loader_mime_type_strategy(
        mock_blob_loader,
        mock_html_parser_class,
        mock_pdf_parser_class,
        mock_text_parser_class,
        mock_csv_parser_class,
        mock_rtf_parser_class,
        mock_md_parser_class,
        mock_email_parser_class,
        mock_docx_parser_class,
        mock_ppt_parser_class,
        mock_get_default_handlers,
        mock_guess_type,
        mock_isfile,
        file_path,
        expected_mime,
):
    mock_guess_type.return_value = (expected_mime, None)

    # Mock blob and blob loader
    mock_blob = MagicMock()
    mock_blob.path = file_path
    mock_blob_loader_instance = MagicMock()
    mock_blob_loader_instance.yield_blobs.return_value = [mock_blob]
    mock_blob_loader.return_value = mock_blob_loader_instance

    # Create parser mock instance
    mock_parser_instance = MagicMock()
    mock_parser_instance.lazy_parse.return_value = [Document(page_content="Mock content")]

    # Set up mock handlers
    mock_handlers = {
        "text/plain": mock_text_parser_class.return_value,
        "text/csv": mock_csv_parser_class.return_value,
        "application/pdf": mock_pdf_parser_class.return_value,
        "text/html": mock_html_parser_class.return_value,
        "application/rtf": mock_rtf_parser_class.return_value,
        "text/markdown": mock_md_parser_class.return_value,
        "application/vnd.ms-outlook": mock_email_parser_class.return_value,
        "message/rfc822": mock_email_parser_class.return_value,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": mock_docx_parser_class.return_value,
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": mock_ppt_parser_class.return_value,
    }
    mock_get_default_handlers.return_value = mock_handlers

    # Configure parser class mocks to return our instance
    mock_text_parser_class.return_value = mock_parser_instance
    mock_csv_parser_class.return_value = mock_parser_instance
    mock_pdf_parser_class.return_value = mock_parser_instance
    mock_html_parser_class.return_value = mock_parser_instance
    mock_rtf_parser_class.return_value = mock_parser_instance
    mock_md_parser_class.return_value = mock_parser_instance
    mock_email_parser_class.return_value = mock_parser_instance
    mock_docx_parser_class.return_value = mock_parser_instance
    mock_ppt_parser_class.return_value = mock_parser_instance

    # Create loader
    loader = UniversalDocumentLoader(file_path)

    # Get the docs
    docs = loader.load()

    assert isinstance(docs, list)
    assert len(docs) > 0
    assert isinstance(docs[0], Document)

    # Verify the correct parser was called
    if expected_mime in mock_handlers:
        mock_parser_instance.lazy_parse.assert_called_once_with(mock_blob)
    else:
        mock_text_parser_class.return_value.lazy_parse.assert_called_once_with(mock_blob)