<p align="center">
  <img src="logo.png" alt="TallyBridge Logo" width="400"/>
</p>


# TallyBridge

> **Version 2.0.0 (Streamlit Web App)** – Convert your bank statement PDFs to Tally-compatible XML with a modern, interactive web interface.

---

## 🚀 What's New in v2.0.0
- 🌐 **Streamlit Web UI**: Upload PDFs, preview & edit vouchers, and download XML directly from your browser
- 📝 **Editable Table**: Review, edit, or delete extracted vouchers before generating XML
- 📈 **Opening & Closing Balance**: Instantly see your statement's opening and closing balances
- ⚡ **No CLI Needed**: Everything works in your browser—no command-line required
- 🏦 **SBI Support**: SBI bank statements fully supported (more banks coming soon)
- 🛠️ **Configurable**: Set Tally ledger names, company, currency, and transaction type in-app
- 🧾 **Tally-Ready XML**: Download XML ready for import into Tally

---


## Features

- 🏦 **Multi-Bank Support** - SBI supported, more banks coming soon
- 🔄 **Automated Processing** - Extract transactions from PDFs automatically
- 📊 **Tally-Ready XML** - Generates perfectly formatted XML for direct import
- ⚙️ **Highly Configurable** - Customize account names, currency, and transaction types
- 💰 **Smart Voucher Generation** - Automatically creates Receipt and Payment vouchers
- ✅ **Double-Entry Bookkeeping** - Maintains proper accounting standards
- 🎯 **Detailed Transaction Records** - Includes narration and bank allocation details
- 🌐 **Web UI** - Edit, preview, and download from your browser


## Requirements

- Python 3.8 or higher
- pip (Python package manager)


## Installation & Quick Start (Web App)

1. Clone this repository:
  ```bash
  git clone https://github.com/visionjain/TallyBridge.git
  cd TallyBridge
  ```
2. Create and activate a virtual environment (recommended):
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Run the Streamlit app:
  ```bash
  streamlit run app.py
  ```
5. Open your browser and go to the URL shown in the terminal (usually http://localhost:8501)


## How to Use (Web App)
1. **Upload your SBI bank statement PDF**
2. **Preview and edit vouchers** in the interactive table
3. **Check opening and closing balances** above the table
4. **Configure Tally details** (ledger names, company, etc.)
5. **Click 'Generate XML'** and download your Tally-ready XML file


## Configuration
- All settings (bank account name, suspense account, currency, company, transaction type) can be set in the web UI
- Settings are saved to `config.json` for future runs

## How It Works

1. **PDF Parsing**: Extracts transaction data (date, amount, description, reference) from PDF tables
2. **Voucher Generation**: Creates Receipt/Payment vouchers based on credit/debit transactions
3. **XML Output**: Generates Tally-compatible XML with proper structure and formatting

Each transaction creates:
- Double-entry voucher (Suspense ↔ Bank Account)
- Proper ALLLEDGERENTRIES with correct signs
- BANKALLOCATIONS with transaction details
- NARRATION with description and reference number


## Project Structure
```
TallyBridge/
├── app.py                 # Streamlit web app (main entry)
├── src/
│   ├── pdf_parser.py      # PDF extraction logic
│   ├── xml_template.py    # XML generation templates
│   ├── xml_from_vouchers.py # XML from table data
│   └── converter.py       # (Legacy CLI converter)
├── config.json            # Saved configuration
├── requirements.txt       # Python dependencies
├── logo.png               # App logo
└── README.md              # This file
```


## Supported Banks
- ✅ State Bank of India (SBI)
- 🔜 HDFC, ICICI, Axis (coming soon)


## Output Format
The generated XML follows Tally's import format:

```xml
<ENVELOPE>
  <HEADER>...</HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDATA>
        <TALLYMESSAGE>
          <LEDGER>...</LEDGER>
          <VOUCHER>...</VOUCHER>
          ...
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```


## Troubleshooting

### PDF Not Parsing Correctly

- Ensure your PDF is from a supported bank (currently SBI)
- Check that the PDF is not password-protected or scanned image
- Verify the PDF contains properly formatted tables with transaction data
- For unsupported banks, please open an issue or contribute a parser

### Import Errors in Tally

- Verify bank account name matches your Tally ledger exactly
- Ensure all required ledgers (Bank, Suspense) exist in Tally
- Check that dates are in correct format (YYYYMMDD)

### Configuration Issues

- Delete `config.json` to reset to defaults
- Run `python src/config_util.py` to reconfigure interactively


## Contributing
We welcome contributions!


## Roadmap
### Current Version (v2.0 - Streamlit Web App)
- ✅ SBI bank statement support
- ✅ PDF to Tally XML conversion
- ✅ Configurable settings
- ✅ Web-based interface
- ✅ Table editing, opening/closing balance, download XML

### Future Banks
- 🔜 HDFC Bank
- 🔜 ICICI Bank
- 🔜 Axis Bank
- 🔜 More banks based on community requests


## 📝 Copyright & License
MIT License © 2025 Vision Jain

---

Made with ❤️ for accountants and businesses using Tally
