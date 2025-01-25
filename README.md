# Frachtauftrag PDF to Excel Converter with Bearer Token Authentication

This Streamlit application allows users to upload a single-page PDF file and convert its extracted transportation data into an Excel file. The application features a basic authentication mechanism using a hardcoded bearer token for secure access.

---

## Features

- **PDF to Excel Conversion**:

  - Upload a single-page PDF file containing transportation data.
  - Extract data from the PDF and transform it into a structured format.
  - Download the extracted data as an Excel file.

- **Authentication**:

  - Secure access to the application using a bearer token.
  - Prevent unauthorized use by validating user tokens.

- **Data Processing**:
  - Extract structured transportation data such as starting location, type of trip (e.g., "Leerfahrt", "Beladen"), and the number of pallets.
  - Supports intelligent processing to consolidate repeated entries for the same location.

---

## Requirements

### Install Dependencies

All required libraries are listed in the `requirements.txt` file. Install them with:

```bash
pip install -r requirements.txt
```
