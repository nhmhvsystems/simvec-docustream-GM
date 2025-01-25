from io import BytesIO

from PyPDF2 import PdfReader


def is_single_page_pdf(pdf_bytes):
    """
    Checks if the given PDF file has only one page.

    Args:
        pdf_bytes (bytes): The PDF file content as a byte string.

    Returns:
        bool: True if the PDF has only one page, False otherwise.
    """
    pdf_stream = BytesIO(pdf_bytes)
    reader = PdfReader(pdf_stream)
    return len(reader.pages) == 1
