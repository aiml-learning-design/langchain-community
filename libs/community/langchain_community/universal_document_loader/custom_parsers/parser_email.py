from extract_msg import Message as OutlookMsgParser
from langchain_core.document_loaders import BaseBlobParser
from langchain_core.documents import Document
from typing import List


class EmailParser(BaseBlobParser):
    """Parse both EML and MSG files."""

    def lazy_parse(self, blob) -> List[Document]:
        if blob.path.endswith(".msg"):
            return self._parse_msg(blob)
        else:
            return self._parse_eml(blob)

    def _parse_eml(self, blob) -> List[Document]:
        """Parse .eml files using Python's email module."""
        with open(blob.path, "r", encoding="utf-8") as f:
            email = EmailParser().parse(f)

        return [Document(
            page_content=email.get_payload(),
            metadata={
                "subject": email["subject"],
                "from": email["from"],
                "to": email["to"],
                "date": email["date"]
            }
        )]

    def _parse_msg(self, blob) -> List[Document]:
        """Parse Outlook .msg files using extract_msg."""
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
