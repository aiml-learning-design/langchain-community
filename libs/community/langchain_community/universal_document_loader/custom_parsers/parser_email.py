from extract_msg import Message as OutlookMsgParser
from langchain_core.document_loaders import BaseBlobParser
from langchain_core.documents import Document
from typing import List
import email


class EmailParser(BaseBlobParser):
    """
    A document parser for email files supporting both `.eml` and `.msg` formats.

    - `.eml` files are parsed using Python’s built-in `email` module.
    - `.msg` files (Outlook format) are parsed using the `extract_msg` library.

    Returns a list of LangChain `Document` objects containing the message body and metadata.
    """

    def lazy_parse(self, blob) -> List[Document]:
        """
        Lazily parse the given email blob (either `.eml` or `.msg`) into a list of `Document`.

        Args:
            blob: A blob object representing the email file.

        Returns:
            List[Document]: A list containing a single parsed document with content and metadata.
        """
        if blob.path.endswith(".msg"):
            return self._parse_msg(blob)
        else:
            return self._parse_eml(blob)

    def _parse_eml(self, blob) -> List[Document]:
        """
        Parse an `.eml` file using the built-in `email` module.

        Args:
            blob: A blob object pointing to an `.eml` file.

        Returns:
            List[Document]: A document containing the email body and metadata.
        """
        with open(blob.path, "r", encoding="utf-8") as f:
            parsed_email = email.message_from_file(f)

        return [Document(
            page_content=parsed_email.get_payload(),
            metadata={
                "subject": parsed_email["subject"],
                "from": parsed_email["from"],
                "to": parsed_email["to"],
                "date": parsed_email["date"]
            }
        )]

    def _parse_msg(self, blob) -> List[Document]:
        """
        Parse an Outlook `.msg` file using the `extract_msg` library.

        Args:
            blob: A blob object pointing to a `.msg` file.

        Returns:
            List[Document]: A document containing the email body and metadata.
        """
        msg = OutlookMsgParser(blob.path)
        return [Document(
            page_content=msg.body,
            metadata={
                "subject": msg.subject,
                "from": msg.sender,
                "to": msg.to,
                "date": msg.date
            }
        )]