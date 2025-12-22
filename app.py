

import streamlit as st

# Set Streamlit page config
st.set_page_config(page_title="tallyBridge", page_icon=":ledger:")
import tempfile
import os
import json
import subprocess
import sys
sys.path.append("src")
from pdf_parser import PDFParser


col1, col2, col3 = st.columns([1.2,2,0.8])
with col2:
    st.image("logo.png", width=260)
st.markdown("<div style='margin-top: -60px; text-align: center;'><p style='font-size: 1.1rem;'>Upload a bank statement PDF to generate Tally-compatible XML.</p></div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
vouchers = None
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name
    # Extract vouchers from PDF
    parser = PDFParser(temp_pdf_path)
    transactions = parser.parse()
    vouchers = [
        {
            "Date": t.txn_date,
            "Type": t.type,
            "Amount": t.amount,
            "Description": t.description,
            "Ref No": t.ref_no,
            "Debit": t.debit,
            "Credit": t.credit,
            "Balance": t.balance
        }
        for t in transactions
    ]
    os.remove(temp_pdf_path)

if vouchers:
    # Show opening and closing balance above the table
    try:
        opening_balance = vouchers[0]["Balance"] if vouchers else None
        closing_balance = vouchers[-1]["Balance"] if vouchers else None
        if opening_balance is not None and closing_balance is not None:
            st.markdown(f"**Opening Balance:** {opening_balance} &nbsp;&nbsp;&nbsp; **Closing Balance:** {closing_balance}")
    except Exception:
        pass
    st.write("### Preview and Edit Vouchers")
    edited_vouchers = st.data_editor(vouchers, num_rows="dynamic", width='stretch')

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
        bank_account_name = st.text_input("Bank Account Name", value="My Bank Account")
        suspense_account_name = st.text_input("Suspense Account Name", value="Suspense")
        currency = st.text_input("Currency", value="₹")
        company_name = st.text_input("Company Name", value="My Company Name")
        default_transaction_type = st.text_input("Default Transaction Type", value="Cheque")

        if st.button("Generate XML"):
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

            from src.xml_from_vouchers import generate_xml_from_vouchers
            with st.spinner("Generating XML from table data..."):
                try:
                    # Use edited_vouchers if available, else fallback to vouchers
                    xml_input = edited_vouchers if 'edited_vouchers' in locals() else vouchers
                    xml_str = generate_xml_from_vouchers(xml_input)
                    st.success("XML generated successfully!")
                    st.download_button(
                        label="Download XML",
                        data=xml_str.encode("utf-8"),
                        file_name="tally_output.xml",
                        mime="application/xml"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
