

import streamlit as st
import tempfile
import os
import json
import subprocess


col1, col2, col3 = st.columns([1.2,2,0.8])
with col2:
    st.image("logo.png", width=260, use_column_width=False)
st.markdown("<div style='margin-top: -60px; text-align: center;'><p style='font-size: 1.1rem;'>Upload a bank statement PDF to generate Tally-compatible XML.</p></div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    st.write("Select your bank:")
    bank_options = ["SBI", "HDFC (coming soon)", "ICICI (coming soon)", "Axis (coming soon)"]
    bank_disabled = [False, True, True, True]
    selected_bank = st.selectbox(
        "Bank",
        options=bank_options,
        index=0,
        help="Only SBI is supported for now. Other banks coming soon."
    )
    if selected_bank != "SBI":
        st.warning("Only SBI is supported for now. Please select SBI.")
    else:
        st.write("Enter Tally configuration details:")
        bank_account_name = st.text_input("Bank Account Name", value="Abhishek Jain(SBI SAVING)")
        suspense_account_name = st.text_input("Suspense Account Name", value="Suspense")
        currency = st.text_input("Currency", value="₹")
        company_name = st.text_input("Company Name", value="Abc Creation")
        default_transaction_type = st.text_input("Default Transaction Type", value="Cheque")

        if st.button("Generate XML"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                temp_pdf_path = temp_pdf.name
            temp_xml_path = temp_pdf_path.replace(".pdf", "_output.xml")

            # Save config to config.json
            config = {
                "bank_account_name": bank_account_name,
                "suspense_account_name": suspense_account_name,
                "currency": currency,
                "company_name": company_name,
                "default_transaction_type": default_transaction_type
            }
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            with st.spinner("Processing PDF and generating XML..."):
                try:
                    # Run converter as subprocess
                    result = subprocess.run([
                        "python", "-m", "src.converter", temp_pdf_path, temp_xml_path
                    ], capture_output=True, text=True)
                    if result.returncode != 0:
                        st.error(f"Error: {result.stderr}")
                    else:
                        with open(temp_xml_path, "rb") as f:
                            xml_data = f.read()
                        st.success("XML generated successfully!")
                        st.download_button(
                            label="Download XML",
                            data=xml_data,
                            file_name="tally_output.xml",
                            mime="application/xml"
                        )
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    os.remove(temp_pdf_path)
                    if os.path.exists(temp_xml_path):
                        os.remove(temp_xml_path)
