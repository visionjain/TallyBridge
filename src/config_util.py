#!/usr/bin/env python3
"""
Configuration Utility
Easily update bank account name and other settings
"""

import json
import os
import sys

# Get config file path relative to project root
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

DEFAULT_CONFIG = {
    "bank_account_name": "State Bank of India (CC/OD)",
    "suspense_account_name": "Suspense",
    "currency": "₹",
    "company_name": "Abc Creation",
    "default_transaction_type": "Cheque"
}

def load_config():
    """Load existing config or create default"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def print_config(config):
    """Display current configuration"""
    print("\n" + "="*60)
    print("CURRENT CONFIGURATION")
    print("="*60)
    for i, (key, value) in enumerate(config.items(), 1):
        key_display = key.replace('_', ' ').title()
        print(f"{i}. {key_display:30} : {value}")
    print("="*60)

def main():
    print("\n" + "="*60)
    print(" "*15 + "TALLY CONVERTER CONFIG")
    print("="*60)
    
    config = load_config()
    print_config(config)
    
    print("\nOptions:")
    print("  1. Change Bank Account Name")
    print("  2. Change Suspense Account Name")
    print("  3. Change Currency")
    print("  4. Change Company Name")
    print("  5. Change Transaction Type")
    print("  6. Reset to Defaults")
    print("  0. Exit")
    
    choice = input("\nSelect option (0-6): ").strip()
    
    if choice == '1':
        new_value = input("\nEnter new bank account name: ").strip()
        if new_value:
            config['bank_account_name'] = new_value
            save_config(config)
            print(f"✓ Bank account name updated to: {new_value}")
    
    elif choice == '2':
        new_value = input("\nEnter new suspense account name: ").strip()
        if new_value:
            config['suspense_account_name'] = new_value
            save_config(config)
            print(f"✓ Suspense account name updated to: {new_value}")
    
    elif choice == '3':
        new_value = input("\nEnter new currency symbol: ").strip()
        if new_value:
            config['currency'] = new_value
            save_config(config)
            print(f"✓ Currency updated to: {new_value}")
    
    elif choice == '4':
        new_value = input("\nEnter new company name: ").strip()
        if new_value:
            config['company_name'] = new_value
            save_config(config)
            print(f"✓ Company name updated to: {new_value}")
    
    elif choice == '5':
        print("\nCommon transaction types:")
        print("  - Cheque")
        print("  - NEFT")
        print("  - RTGS")
        print("  - IMPS")
        print("  - UPI")
        new_value = input("\nEnter new transaction type: ").strip()
        if new_value:
            config['default_transaction_type'] = new_value
            save_config(config)
            print(f"✓ Transaction type updated to: {new_value}")
    
    elif choice == '6':
        confirm = input("\nReset to default configuration? (y/N): ").strip().lower()
        if confirm == 'y':
            save_config(DEFAULT_CONFIG)
            print("✓ Configuration reset to defaults")
    
    elif choice == '0':
        print("\nExiting...")
        return
    
    else:
        print("\n❌ Invalid option")
        return
    
    # Show updated config
    config = load_config()
    print_config(config)
    
    print("\n✓ Configuration saved to config.json")
    print("You can now run the converter with these settings.\n")

if __name__ == "__main__":
    main()
