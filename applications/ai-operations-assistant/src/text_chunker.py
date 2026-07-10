from typing import Any


def chunk_pages(
    pages: list[dict[str, Any]],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[dict[str, Any]]:
    """
    Split page text into overlapping character-based chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []
    chunk_id = 1
    step = chunk_size - chunk_overlap

    for page in pages:

        text = page.get("text", "").strip()
        page_number = page.get("page_number")

        if not text:
            continue

        for start in range(0, len(text), step):

            chunk_text = text[start:start + chunk_size]

            if not chunk_text:
                continue

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "page_number": page_number,
                    "text": chunk_text,
                    "start_character": start,
                    "end_character": start + len(chunk_text),
                }
            )

            chunk_id += 1

            if start + chunk_size >= len(text):
                break

    return chunks