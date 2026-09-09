"""
PDF Parser Module
Extracts transaction data from SBI bank statement PDFs
"""

import pdfplumber
import re
from datetime import datetime
from typing import List, Dict
import html


class Transaction:
    """Represents a single bank transaction"""
    
    def __init__(self, txn_date, value_date, description, ref_no, debit, credit, balance):
        self.txn_date = txn_date
        self.value_date = value_date
        self.description = description
        self.ref_no = ref_no
        self.debit = debit
        self.credit = credit
        self.balance = balance
        
        # Determine transaction type
        if debit and float(debit.replace(',', '')) > 0:
            self.type = "Payment"
            self.amount = float(debit.replace(',', ''))
        elif credit and float(credit.replace(',', '')) > 0:
            self.type = "Receipt"
            self.amount = float(credit.replace(',', ''))
        else:
            self.type = "Unknown"
            self.amount = 0.0
    
    def get_tally_date(self):
        """Convert date to Tally format YYYYMMDD"""
        try:
            date_clean = self.txn_date.replace('\n', ' ').strip()
            for fmt in ("%d/%m/%Y", "%d %b %Y"):
                try:
                    return datetime.strptime(date_clean, fmt).strftime("%Y%m%d")
                except ValueError:
                    pass
            return ""
        except Exception:
            return ""
    
    def get_narration(self):
        """Generate narration for Tally voucher"""
        # Keep original format - don't modify newlines
        # Description already has dashes from PDF where needed
        narration = f"{self.description} &amp; {self.ref_no}"
        return narration
    
    def get_instrument_number(self):
        """Extract instrument number from ref_no"""
        return self.ref_no.replace('\n', '\n')
    
    def __repr__(self):
        return f"Transaction({self.txn_date}, {self.type}, {self.amount})"


class PDFParser:
    """Parse SBI bank statement PDF and extract transactions"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.transactions: List[Transaction] = []
    
    def parse(self) -> List[Transaction]:
        """Parse PDF and extract all transactions"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                print(f"Processing page {page_num + 1}/{len(pdf.pages)}...")
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    # Check if this is the transaction table
                    header = table[0]
                    if self._is_transaction_table(header):
                        # Process transaction rows (skip header)
                        for row in table[1:]:
                            txn = self._parse_transaction_row(row)
                            if txn:
                                self.transactions.append(txn)
        
        print(f"Extracted {len(self.transactions)} transactions")
        return self.transactions
    
    def _is_transaction_table(self, header: List) -> bool:
        """Check if table header matches transaction table format"""
        if not header or len(header) < 5:
            return False

        header_str = ' '.join([str(h).lower() if h else '' for h in header])
        # Standard format with explicit column headers
        if ('txn date' in header_str or 'transaction date' in header_str) and \
               ('debit' in header_str or 'credit' in header_str):
            return True
        # SBI format: 7 columns, last header is "Balance", no explicit date column label
        if len(header) == 7 and str(header[-1]).strip().lower() == 'balance':
            return True
        return False
    
    def _parse_transaction_row(self, row: List) -> Transaction:
        """Parse a single transaction row from the table"""
        try:
            # Expected format: [Txn Date, Value Date, Description, Ref No, Debit, Credit, Balance]
            if not row or len(row) < 7:
                return None

            txn_date = self._clean_value(row[0])
            value_date = self._clean_value(row[1])
            description = self._clean_value(row[2])
            ref_no = self._clean_value(row[3])
            debit = self._clean_amount(row[4])
            credit = self._clean_amount(row[5])
            balance = self._clean_value(row[6])

            # Skip if no date (likely a header or empty row)
            if not txn_date or not self._is_valid_date(txn_date):
                return None

            # Skip if no debit or credit amount
            if not debit and not credit:
                return None

            return Transaction(txn_date, value_date, description, ref_no,
                             debit or '', credit or '', balance)
        except Exception as e:
            print(f"Error parsing row: {e}")
            return None
    
    def _clean_value(self, value) -> str:
        """Clean and normalize cell value"""
        if value is None:
            return ''
        return str(value).strip()

    def _clean_amount(self, value) -> str:
        """Clean amount cell — treat '-' as empty (SBI uses '-' for no transaction)"""
        v = self._clean_value(value)
        return '' if v == '-' else v

    def _is_valid_date(self, date_str: str) -> bool:
        """Check if string looks like a valid date"""
        date_clean = date_str.replace('\n', ' ').strip()
        for fmt in ("%d/%m/%Y", "%d %b %Y"):
            try:
                datetime.strptime(date_clean, fmt)
                return True
            except ValueError:
                pass
        return False
    
    def get_transactions(self) -> List[Transaction]:
        """Get list of parsed transactions"""
        return self.transactions
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Transaction]:
        """Filter transactions by date range (format: YYYY-MM-DD)"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        filtered = []
        for txn in self.transactions:
            try:
                date_clean = txn.txn_date.replace('\n', ' ').strip()
                txn_dt = None
                for fmt in ("%d/%m/%Y", "%d %b %Y"):
                    try:
                        txn_dt = datetime.strptime(date_clean, fmt)
                        break
                    except ValueError:
                        pass
                if txn_dt and start <= txn_dt <= end:
                    filtered.append(txn)
            except:
                continue
        
        return filtered
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        total_debits = sum(t.amount for t in self.transactions if t.type == "Payment")
        total_credits = sum(t.amount for t in self.transactions if t.type == "Receipt")
        
        return {
            'total_transactions': len(self.transactions),
            'payments': sum(1 for t in self.transactions if t.type == "Payment"),
            'receipts': sum(1 for t in self.transactions if t.type == "Receipt"),
            'total_debits': total_debits,
            'total_credits': total_credits,
            'net': total_credits - total_debits
        }


if __name__ == "__main__":
    # Test the parser
    parser = PDFParser("cc 1-4-25 to 13-9-25.pdf")
    transactions = parser.parse()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    summary = parser.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*80)
    print("FIRST 10 TRANSACTIONS")
    print("="*80)
    for i, txn in enumerate(transactions[:10]):
        print(f"{i+1}. {txn.txn_date} | {txn.type} | ₹{txn.amount:,.2f}")
        print(f"   Description: {txn.description[:60]}...")
        print()
