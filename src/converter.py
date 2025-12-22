"""
PDF to Tally XML Converter
Main application to convert SBI bank statement PDF to Tally XML format
"""

import sys
import os
import json
from .pdf_parser import PDFParser
from .xml_template import (
    get_xml_header, 
    get_suspense_ledger, 
    generate_voucher, 
    get_xml_footer,
    load_config
)


class TallyConverter:
    """Convert bank statement PDF to Tally XML"""
    
    def __init__(self, pdf_path: str, output_path: str = None):
        self.pdf_path = pdf_path
        self.output_path = output_path or self._generate_output_filename()
        self.parser = PDFParser(pdf_path)
        self.transactions = []
    
    def _generate_output_filename(self) -> str:
        """Generate output filename based on input PDF"""
        base = os.path.splitext(self.pdf_path)[0]
        return f"{base}_tally.xml"
    
    def convert(self):
        """Main conversion process"""
        print("="*80)
        print("PDF TO TALLY XML CONVERTER")
        print("="*80)
        
        # Show configuration
        config = load_config()
        print(f"\nConfiguration:")
        print(f"  Bank Account: {config['bank_account_name']}")
        print(f"  Suspense Account: {config['suspense_account_name']}")
        
        print(f"\nInput PDF: {self.pdf_path}")
        print(f"Output XML: {self.output_path}")
        
        # Step 1: Parse PDF
        print("\n[1/3] Parsing PDF...")
        self.transactions = self.parser.parse()
        
        if not self.transactions:
            print("❌ No transactions found in PDF!")
            return False
        
        # Show summary
        summary = self.parser.get_summary()
        print(f"\n✓ Found {summary['total_transactions']} transactions")
        print(f"  - Payments: {summary['payments']}")
        print(f"  - Receipts: {summary['receipts']}")
        print(f"  - Total Debits: ₹{summary['total_debits']:,.2f}")
        print(f"  - Total Credits: ₹{summary['total_credits']:,.2f}")
        
        # Step 2: Generate XML
        print("\n[2/3] Generating Tally XML...")
        xml_content = self._generate_xml()
        
        # Step 3: Write to file
        print("\n[3/3] Writing XML file...")
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"✓ XML file created successfully!")
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False
        
        # Final summary
        file_size = os.path.getsize(self.output_path) / 1024  # KB
        print("\n" + "="*80)
        print("CONVERSION COMPLETE")
        print("="*80)
        print(f"Output file: {self.output_path}")
        print(f"File size: {file_size:.2f} KB")
        print(f"Total vouchers: {len(self.transactions)}")
        print("\n✓ Ready to import into Tally!")
        print("="*80)
        
        return True
    
    def _generate_xml(self) -> str:
        """Generate complete Tally XML from transactions"""
        xml_parts = []
        
        # Add header
        xml_parts.append(get_xml_header())
        
        # Add Suspense ledger (master data)
        xml_parts.append(get_suspense_ledger())
        
        # Add vouchers for each transaction
        alter_id = 4
        master_id = 3
        
        for i, txn in enumerate(self.transactions):
            tally_date = txn.get_tally_date()
            if not tally_date:
                continue
            
            narration = txn.get_narration()
            instrument_number = txn.get_instrument_number()
            
            voucher_xml = generate_voucher(
                txn_date=tally_date,
                voucher_type=txn.type,
                narration=narration,
                amount=txn.amount,
                instrument_number=instrument_number,
                alter_id=alter_id,
                master_id=master_id
            )
            
            xml_parts.append(voucher_xml)
            
            # Increment IDs (some transactions share same IDs in original)
            if i % 2 == 1:  # Increment every 2 transactions
                alter_id += 1
                master_id += 1
        
        # Add footer
        xml_parts.append(get_xml_footer())
        
        return ''.join(xml_parts)
    
    def validate_output(self, original_xml: str = None):
        """Compare output with original XML for validation"""
        if not original_xml or not os.path.exists(original_xml):
            print("\n⚠ No original XML provided for validation")
            return
        
        print("\n" + "="*80)
        print("VALIDATION")
        print("="*80)
        
        # Compare file sizes
        original_size = os.path.getsize(original_xml) / 1024
        output_size = os.path.getsize(self.output_path) / 1024
        
        print(f"Original XML: {original_size:.2f} KB")
        print(f"Generated XML: {output_size:.2f} KB")
        print(f"Size difference: {abs(original_size - output_size):.2f} KB")
        
        # Count vouchers in both files
        with open(original_xml, 'r', encoding='utf-8') as f:
            original_content = f.read()
            original_vouchers = original_content.count('<VOUCHER VCHTYPE=')
        
        with open(self.output_path, 'r', encoding='utf-8') as f:
            output_content = f.read()
            output_vouchers = output_content.count('<VOUCHER VCHTYPE=')
        
        print(f"\nOriginal vouchers: {original_vouchers}")
        print(f"Generated vouchers: {output_vouchers}")
        
        if output_vouchers == original_vouchers:
            print("✓ Voucher count matches!")
        else:
            print(f"⚠ Difference: {abs(original_vouchers - output_vouchers)} vouchers")


def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python converter.py <pdf_file> [output_xml] [--bank-name \"Your Bank Name\"]")
        print("\nExample:")
        print("  python converter.py 'statement.pdf'")
        print("  python converter.py 'statement.pdf' output.xml")
        print("  python converter.py 'statement.pdf' output.xml --bank-name \"SBI CC Account\"")
        print("\nOr edit config.json to set default bank name")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = None
    bank_name = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--bank-name' and i + 1 < len(sys.argv):
            bank_name = sys.argv[i + 1]
            i += 2
        elif not output_file and not sys.argv[i].startswith('--'):
            output_file = sys.argv[i]
            i += 1
        else:
            i += 1
    
    # Update config if bank name provided
    if bank_name:
        # Get config path relative to project root
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(script_dir, 'config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            config['bank_account_name'] = bank_name
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"✓ Updated bank account name to: {bank_name}")
        except Exception as e:
            print(f"Warning: Could not update config: {e}")
    
    # Check if PDF exists
    if not os.path.exists(pdf_file):
        print(f"❌ Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    # Create converter and run
    converter = TallyConverter(pdf_file, output_file)
    success = converter.convert()
    
    # Optionally validate against original
    original_xml = "cc_1-4-25_to_13-9-25.xml"
    if os.path.exists(original_xml):
        converter.validate_output(original_xml)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
