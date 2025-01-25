import base64
from io import BytesIO

import pymupdf


def pdf_to_base64_url(pdf_bytes, dpi=300):
    """
    Convert a PDF file to a Base64-encoded PNG URL.

    This function takes the bytes of a PDF file and converts the first page of the PDF into a PNG image.
    The image is encoded as a Base64 string and returned as a data URL.

    Args:
        pdf_bytes (bytes): The byte content of the PDF file.
        dpi (int, optional): The resolution for rendering the PDF page as an image. Default is 300 DPI.

    Returns:
        str: A Base64-encoded data URL representing the PNG image of the first page of the PDF.
    """
    pdf_stream = BytesIO(pdf_bytes)
    doc = pymupdf.open(stream=pdf_stream)
    pix = doc[0].get_pixmap(dpi=dpi)
    image_bytes = pix.tobytes("png")
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{base64_image}"
