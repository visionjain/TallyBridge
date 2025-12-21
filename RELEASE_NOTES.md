# Release Notes

## Version 1.0.0 - Initial Release
**Release Date:** December 22, 2025

### 🎉 Introduction

We're excited to announce the first stable release of **TallyBridge** - a powerful command-line tool that bridges the gap between bank statements and Tally accounting software.

### ✨ Features

#### Core Functionality
- **PDF to XML Conversion** - Automatically extract transactions from bank statement PDFs
- **Tally-Ready Output** - Generate XML files that can be directly imported into Tally ERP 9 / TallyPrime
- **Double-Entry Bookkeeping** - Maintains proper accounting standards with suspense and bank accounts
- **Smart Voucher Generation** - Automatically creates Receipt and Payment vouchers based on transaction type

#### Bank Support
- ✅ **State Bank of India (SBI)** - Full support for SBI bank statement PDFs
  - Extracts date, amount, description, and reference numbers
  - Handles both debit and credit transactions
  - Processes multi-page statements

#### Configuration & Customization
- **Configurable Settings** - Customize via `config.json` or command-line arguments
- **Bank Account Name** - Set custom bank account ledger name
- **Suspense Account** - Configure temporary ledger name
- **Currency Support** - Default ₹ (Indian Rupee)
- **Transaction Types** - Configure default transaction type (Cheque, NEFT, etc.)

#### Technical Features
- **Proper XML Structure** - Follows Tally XML import specifications exactly
- **LEDGER Generation** - Creates suspense ledger with all required fields
- **BANKALLOCATIONS** - Includes transaction details with instrument number and date
- **NARRATION** - Preserves transaction description and reference numbers
- **Proper Amount Signs** - Correct positive/negative values for receipts and payments

### 📦 Installation

```bash
git clone https://github.com/visionjain/TallyBridge.git
cd TallyBridge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp config.json.example config.json
```

### 🚀 Usage

Basic conversion:
```bash
python tally_converter.py input.pdf output.xml
```

With custom bank name:
```bash
python tally_converter.py input.pdf output.xml --bank-name "Your Bank Account"
```

Interactive configuration:
```bash
python src/config_util.py
```

### 📋 Requirements

- Python 3.8 or higher
- pdfplumber 0.10.3+
- pandas 2.0.0+
- python-dateutil 2.8.2+

### 🐛 Known Issues

- Currently supports only SBI bank statement format
- PDF must be text-based (not scanned images)
- Large PDFs (100+ pages) may take longer to process

### 🔜 What's Next?

Version 2.0 will bring exciting new features:
- Web-based user interface
- Drag-and-drop PDF upload
- Support for multiple banks (HDFC, ICICI, Axis)
- Batch processing
- Real-time preview

### 📝 Copyright & License

**Copyright © 2025 Vision Jain. All rights reserved.**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📞 Support

- **Issues:** [GitHub Issues](https://github.com/visionjain/TallyBridge/issues)
- **Documentation:** See [README.md](README.md)
- **Questions:** Open a discussion on GitHub

---

**Download:** [v1.0.0 Release](https://github.com/visionjain/TallyBridge/releases/tag/v1.0.0)

Made with ❤️ for the accounting community
