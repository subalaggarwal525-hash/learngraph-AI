import os
from typing import List, Dict, Any

class DocumentParser:
    @staticmethod
    def parse_file(file_path: str, filename: str) -> Dict[str, Any]:
        ext = os.path.splitext(filename)[1].lower()
        text_content = ""
        sections = []

        if ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        sections.append({"section_title": f"Page {page_num + 1}", "content": page_text.strip()})
                text_content = "\n\n".join([s["content"] for s in sections])
            except Exception as e:
                text_content = f"PDF Error: {e}"
                sections = [{"section_title": "Overview", "content": text_content}]
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()
            sections = [{"section_title": "Section 1", "content": text_content[:1500]}]

        return {"filename": filename, "total_chars": len(text_content), "sections": sections}
