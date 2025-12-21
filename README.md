<p align="center">
  <img src="logo.png" alt="TallyBridge Logo" width="200"/>
</p>

# TallyBridge

> **Version 1.0.0 (Python CLI)** - Bridge the gap between your bank statements and Tally accounting software.

Automatically convert bank statement PDFs to Tally-compatible XML format with this command-line tool.

**📢 Coming Soon:** Web-based version with enhanced UI and additional features!

## Features

- 🏦 **Multi-Bank Support** - Currently supports SBI, with more banks coming soon
- 🔄 **Automated Processing** - Extract transactions from PDFs automatically
- 📊 **Tally-Ready XML** - Generates perfectly formatted XML for direct import
- ⚙️ **Highly Configurable** - Customize account names, currency, and transaction types
- 💰 **Smart Voucher Generation** - Automatically creates Receipt and Payment vouchers
- ✅ **Double-Entry Bookkeeping** - Maintains proper accounting standards
- 🎯 **Detailed Transaction Records** - Includes narration and bank allocation details

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

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

## Usage

### Basic Conversion

```bash
python tally_converter.py input.pdf output.xml
```

### With Custom Bank Name

```bash
python tally_converter.py input.pdf output.xml --bank-name "Your Bank Account Name"
```

### Configure Settings

Edit `config.json` or use the interactive configuration tool:

```bash
python src/config_util.py
```

## Configuration

The `config.json` file contains the following settings:

```json
{
    "bank_account_name": "Your Bank Account",
    "suspense_account_name": "Suspense",
    "currency": "₹",
    "company_name": "Your Company Name",
    "default_transaction_type": "Cheque"
}
```

- **bank_account_name**: The name of your bank account ledger in Tally
- **suspense_account_name**: Temporary ledger name for unallocated transactions
- **currency**: Currency symbol for display
- **company_name**: Your company name (for reference)
- **default_transaction_type**: Default transaction type (Cheque, NEFT, etc.)

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
├── src/
│   ├── converter.py        # Main conversion logic
│   ├── pdf_parser.py       # PDF extraction module
│   ├── xml_template.py     # XML generation templates
│   └── config_util.py      # Configuration utility
├── tally_converter.py      # Main entry point
├── config.json.example     # Configuration template
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # This file
```

## Supported Banks

Currently supported:
- ✅ **State Bank of India (SBI)** - Full support

Coming soon:
- 🔜 HDFC Bank
- 🔜 ICICI Bank
- 🔜 Axis Bank
- 🔜 Other major banks

Want to add support for your bank? Contributions are welcome!

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

### Current Version (v1.0 - Python CLI)
- ✅ SBI bank statement support
- ✅ PDF to Tally XML conversion
- ✅ Configurable settings
- ✅ Command-line interface

### Future Banks
- 🔜 HDFC Bank
- 🔜 ICICI Bank
- 🔜 Axis Bank
- 🔜 More banks based on community requests

## 📝 Copyright & License

**Copyright © 2025 Vision Jain. All rights reserved.**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for accountants and businesses using Tally
