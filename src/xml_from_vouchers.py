import os
import json
from src.xml_template import get_xml_header, get_suspense_ledger, generate_voucher, get_xml_footer, load_config

def generate_xml_from_vouchers(vouchers, output_path=None):
    """
    Generate Tally XML from a list of voucher dicts and save to output_path (if provided).
    Returns the XML string.
    """
    config = load_config()
    xml_parts = [get_xml_header(), get_suspense_ledger()]
    alter_id = 4
    master_id = 3
    for i, v in enumerate(vouchers):
        # Defensive: fallback for missing/invalid fields
        try:
            txn_date = v.get("Date") or v.get("txn_date")
            # Convert to Tally YYYYMMDD format if not already
            if txn_date and len(txn_date) != 8:
                from datetime import datetime
                for fmt in ("%d/%m/%Y", "%d %b %Y"):
                    try:
                        txn_date = datetime.strptime(txn_date, fmt).strftime("%Y%m%d")
                        break
                    except Exception:
                        pass
            voucher_type = v.get("Type") or v.get("type")
            narration = f"{v.get('Description','')} &amp; {v.get('Ref No','')}"
            amount = float(v.get("Amount") or 0)
            instrument_number = v.get("Ref No") or v.get("ref_no") or ""
        except Exception:
            continue
        voucher_xml = generate_voucher(
            txn_date=txn_date,
            voucher_type=voucher_type,
            narration=narration,
            amount=amount,
            instrument_number=instrument_number,
            alter_id=alter_id,
            master_id=master_id
        )
        xml_parts.append(voucher_xml)
        if i % 2 == 1:
            alter_id += 1
            master_id += 1
    xml_parts.append(get_xml_footer())
    xml_str = ''.join(xml_parts)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
    return xml_str
