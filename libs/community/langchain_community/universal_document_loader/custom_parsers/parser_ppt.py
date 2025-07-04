from langchain_core.document_loaders import BaseBlobParser
from pptx import Presentation  # For PPTX
from langchain_core.documents import Document
from typing import List


class PowerPointParser(BaseBlobParser):
    """Parse PPTX (and fallback for PPT)."""

    def lazy_parse(self, blob) -> List[Document]:
        if blob.path.endswith(".pptx"):
            return self._parse_pptx(blob)
        else:
            return self._parse_fallback(blob)

    def _parse_pptx(self, blob) -> List[Document]:
        """Extract text from PPTX slides."""
        prs = Presentation(blob.path)
        text_content = []

        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_content.append(shape.text)

        return [Document(
            page_content="\n".join(text_content),
            metadata={"source": blob.path, "slides": len(prs.slides)}
        )]

    def _parse_fallback(self, blob) -> List[Document]:
        """Fallback for PPT (legacy) or unsupported formats."""
        # Option 1: Convert PPT to PPTX first (requires external tools)
        # Option 2: Use pywin32 (Windows-only)
        # Option 3: Extract raw text (basic)
        with open(blob.path, "rb") as f:
            raw_text = str(f.read(1024))  # Read first 1KB as fallback
        return [Document(page_content=raw_text, metadata={"source": blob.path})]
