# Frachtauftrag PDF to Excel Converter with Bearer Token Authentication.
#
# This Streamlit application allows users to upload a single-page PDF file and convert its extracted data into an Excel file.
# It includes a basic authentication mechanism using a hardcoded bearer token.

import io

import pandas as pd
import streamlit as st
import xlsxwriter

from utils.check_input import is_single_page_pdf
from utils.convert_pdf import pdf_to_base64_url
from utils.data_extraction import extract_data_from_image

# Hardcoded bearer token
VALID_TOKEN = "IQgOKgOg4JVTqw9HMd3qj7uexxO18ZfNpqqzGBYGkuo"


# Authentication function
def authenticate(token):
    return token == VALID_TOKEN


# Check authentication status in session state
def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


# Authentication page
def login_page():
    st.title("Login")
    token = st.text_input("Enter Bearer Token", type="password")

    if st.button("Login"):
        if authenticate(token):
            st.session_state.authenticated = True
            st.success("Login Successful!")
            st.rerun()  # Updated from experimental_rerun()
        else:
            st.error("Invalid token. Access denied.")


# Main application
def main_app():
    st.title("Frachtauftrag PDF to Excel Converter")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            pdf_bytes = uploaded_file.read()

            is_single_page = is_single_page_pdf(pdf_bytes)

            if is_single_page:
                base64_url = pdf_to_base64_url(pdf_bytes)

                extracted_data = extract_data_from_image(base64_url)
                df = pd.DataFrame(extracted_data)
                st.dataframe(df)

                filename = uploaded_file.name
                file_extension = ".pdf"
                filename_without_ext = filename[: -len(file_extension)]

                new_filename = f"{filename_without_ext}.xlsx"

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, sheet_name="Sheet1", index=None)
                    writer.close()
                    st.download_button(
                        label="Download in Excel",
                        data=buffer,
                        file_name=new_filename,
                        mime="application/vnd.ms-excel",
                    )

            else:
                st.error("Please upload a PDF file with only one page.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")


# Application entry point
def app():
    check_auth()

    if not st.session_state.authenticated:
        login_page()
    else:
        col1, col2 = st.columns([9, 1])
        with col1:
            main_app()
        with col2:
            if st.button("Log Out"):
                st.session_state.authenticated = False
                st.rerun()  # Updated from experimental_rerun()


# Run the app
if __name__ == "__main__":
    app()
