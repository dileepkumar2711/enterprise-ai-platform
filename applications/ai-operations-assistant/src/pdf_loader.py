from pathlib import Path
from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "certified-forward-deployed-engineer-cfde.pdf"


def load_pdf(pdf_path: Path) -> list[dict]:
    """Extract text from a PDF and return page-level records."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: list[dict] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip(),
            }
        )

    return pages


if __name__ == "__main__":
    extracted_pages = load_pdf(PDF_PATH)

    print(f"PDF: {PDF_PATH.name}")
    print(f"Total pages: {len(extracted_pages)}")

    for page in extracted_pages:
        print("=" * 60)
        print(f"Page {page['page_number']}")
        print("=" * 60)
        print(page["text"][:1000] or "No text found.")