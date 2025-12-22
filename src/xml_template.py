"""
Tally XML Template Generator
Generates Tally-compliant XML vouchers from transaction data
"""

import json
import os

# Default configuration
DEFAULT_CONFIG = {
    "bank_account_name": "My Bank Account",
    "suspense_account_name": "My Suspense Ledger",
    "currency": "INR",
    "company_name": "My Company Name",
    "default_transaction_type": "Cheque"
}

def load_config():
    """Load configuration from config.json or use defaults"""
    # Look for config.json in project root (one level up from src/)
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults (in case some keys are missing)
                return {**DEFAULT_CONFIG, **config}
        except Exception as e:
            print(f"Warning: Could not load config.json, using defaults. Error: {e}")
    return DEFAULT_CONFIG.copy()

CONFIG = load_config()

def get_xml_header():
    """Generate XML header with envelope and import data structure"""
    return '''<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>

    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
            </STATICVARIABLES>
        </REQUESTDESC>
        <REQUESTDATA>'''


def get_suspense_ledger():
    """Generate Suspense ledger master"""
    config = load_config()
    ledger_name = config['suspense_account_name']
    currency = config['currency']
    company_name = config['company_name']
    
    return f'''
            <TALLYMESSAGE xmlns:UDF="TallyUDF">
                <LEDGER NAME="{ledger_name}" RESERVEDNAME="">
                    <CURRENCYNAME>{currency}</CURRENCYNAME>
                    <PARENT>Suspense A/c</PARENT>
                    <TAXCLASSIFICATIONNAME/>
                    <TAXTYPE>Others</TAXTYPE>
                    <LEDADDLALLOCTYPE/>
                    <GSTTYPE/>
                    <APPROPRIATEFOR/>
                    <SERVICECATEGORY>&#4; Not Applicable</SERVICECATEGORY>
                    <EXCISELEDGERCLASSIFICATION/>
                    <EXCISEDUTYTYPE/>
                    <EXCISENATUREOFPURCHASE/>
                    <LEDGERFBTCATEGORY/>
                    <BANKACCHOLDERNAME>{company_name}</BANKACCHOLDERNAME>
                    <ISBILLWISEON>No</ISBILLWISEON>
                    <ISCOSTCENTRESON>No</ISCOSTCENTRESON>
                    <ISINTERESTON>No</ISINTERESTON>
                    <ALLOWINMOBILE>No</ALLOWINMOBILE>
                    <ISCOSTTRACKINGON>No</ISCOSTTRACKINGON>
                    <ISBENEFICIARYCODEON>No</ISBENEFICIARYCODEON>
                    <ISEXPORTONVCHCREATE>No</ISEXPORTONVCHCREATE>
                    <PLASINCOMEEXPENSE>No</PLASINCOMEEXPENSE>
                    <ISUPDATINGTARGETID>No</ISUPDATINGTARGETID>
                    <ISDELETED>No</ISDELETED>
                    <ISSECURITYONWHENENTERED>No</ISSECURITYONWHENENTERED>
                    <ASORIGINAL>Yes</ASORIGINAL>
                    <ISCONDENSED>No</ISCONDENSED>
                    <AFFECTSSTOCK>No</AFFECTSSTOCK>
                    <ISRATEINCLUSIVEVAT>No</ISRATEINCLUSIVEVAT>
                    <FORPAYROLL>No</FORPAYROLL>
                    <ISABCENABLED>No</ISABCENABLED>
                    <ISCREDITDAYSCHKON>No</ISCREDITDAYSCHKON>
                    <INTERESTONBILLWISE>No</INTERESTONBILLWISE>
                    <OVERRIDEINTEREST>No</OVERRIDEINTEREST>
                    <OVERRIDEADVINTEREST>No</OVERRIDEADVINTEREST>
                    <USEFORVAT>No</USEFORVAT>
                    <IGNORETDSEXEMPT>No</IGNORETDSEXEMPT>
                    <ISTCSAPPLICABLE>No</ISTCSAPPLICABLE>
                    <ISTDSAPPLICABLE>No</ISTDSAPPLICABLE>
                    <ISFBTAPPLICABLE>No</ISFBTAPPLICABLE>
                    <ISGSTAPPLICABLE>No</ISGSTAPPLICABLE>
                    <ISEXCISEAPPLICABLE>No</ISEXCISEAPPLICABLE>
                    <ISTDSEXPENSE>No</ISTDSEXPENSE>
                    <ISEDLIAPPLICABLE>No</ISEDLIAPPLICABLE>
                    <ISRELATEDPARTY>No</ISRELATEDPARTY>
                    <USEFORESIELIGIBILITY>No</USEFORESIELIGIBILITY>
                    <ISINTERESTINCLLASTDAY>No</ISINTERESTINCLLASTDAY>
                    <APPROPRIATETAXVALUE>No</APPROPRIATETAXVALUE>
                    <ISBEHAVEASDUTY>No</ISBEHAVEASDUTY>
                    <INTERESTINCLDAYOFADDITION>No</INTERESTINCLDAYOFADDITION>
                    <INTERESTINCLDAYOFDEDUCTION>No</INTERESTINCLDAYOFDEDUCTION>
                    <ISOTHTERRITORYASSESSEE>No</ISOTHTERRITORYASSESSEE>
                    <IGNOREMISMATCHWITHWARNING>No</IGNOREMISMATCHWITHWARNING>
                    <USEASNOTIONALBANK>No</USEASNOTIONALBANK>
                    <OVERRIDECREDITLIMIT>No</OVERRIDECREDITLIMIT>
                    <ISAGAINSTFORMC>No</ISAGAINSTFORMC>
                    <ISCHEQUEPRINTINGENABLED>Yes</ISCHEQUEPRINTINGENABLED>
                    <ISPAYUPLOAD>No</ISPAYUPLOAD>
                    <ISPAYBATCHONLYSAL>No</ISPAYBATCHONLYSAL>
                    <ISBNFCODESUPPORTED>No</ISBNFCODESUPPORTED>
                    <ALLOWEXPORTWITHERRORS>No</ALLOWEXPORTWITHERRORS>
                    <CONSIDERPURCHASEFOREXPORT>No</CONSIDERPURCHASEFOREXPORT>
                    <ISTRANSPORTER>No</ISTRANSPORTER>
                    <USEFORNOTIONALITC>No</USEFORNOTIONALITC>
                    <ISECOMMOPERATOR>No</ISECOMMOPERATOR>
                    <OVERRIDEBASEDONREALIZATION>No</OVERRIDEBASEDONREALIZATION>
                    <SHOWINPAYSLIP>No</SHOWINPAYSLIP>
                    <USEFORGRATUITY>No</USEFORGRATUITY>
                    <ISTDSPROJECTED>No</ISTDSPROJECTED>
                    <FORSERVICETAX>No</FORSERVICETAX>
                    <ISINPUTCREDIT>No</ISINPUTCREDIT>
                    <ISEXEMPTED>No</ISEXEMPTED>
                    <ISABATEMENTAPPLICABLE>No</ISABATEMENTAPPLICABLE>
                    <ISSTXPARTY>No</ISSTXPARTY>
                    <ISSTXNONREALIZEDTYPE>No</ISSTXNONREALIZEDTYPE>
                    <ISUSEDFORCVD>No</ISUSEDFORCVD>
                    <LEDBELONGSTONONTAXABLE>No</LEDBELONGSTONONTAXABLE>
                    <ISEXCISEMERCHANTEXPORTER>No</ISEXCISEMERCHANTEXPORTER>
                    <ISPARTYEXEMPTED>No</ISPARTYEXEMPTED>
                    <ISSEZPARTY>No</ISSEZPARTY>
                    <TDSDEDUCTEEISSPECIALRATE>No</TDSDEDUCTEEISSPECIALRATE>
                    <ISECHEQUESUPPORTED>No</ISECHEQUESUPPORTED>
                    <ISEDDSUPPORTED>No</ISEDDSUPPORTED>
                    <HASECHEQUEDELIVERYMODE>No</HASECHEQUEDELIVERYMODE>
                    <HASECHEQUEDELIVERYTO>No</HASECHEQUEDELIVERYTO>
                    <HASECHEQUEPRINTLOCATION>No</HASECHEQUEPRINTLOCATION>
                    <HASECHEQUEPAYABLELOCATION>No</HASECHEQUEPAYABLELOCATION>
                    <HASECHEQUEBANKLOCATION>No</HASECHEQUEBANKLOCATION>
                    <HASEDDDELIVERYMODE>No</HASEDDDELIVERYMODE>
                    <HASEDDDELIVERYTO>No</HASEDDDELIVERYTO>
                    <HASEDDPRINTLOCATION>No</HASEDDPRINTLOCATION>
                    <HASEDDPAYABLELOCATION>No</HASEDDPAYABLELOCATION>
                    <HASEDDBANKLOCATION>No</HASEDDBANKLOCATION>
                    <ISEBANKINGENABLED>No</ISEBANKINGENABLED>
                    <ISEXPORTFILEENCRYPTED>No</ISEXPORTFILEENCRYPTED>
                    <ISBATCHENABLED>No</ISBATCHENABLED>
                    <ISPRODUCTCODEBASED>No</ISPRODUCTCODEBASED>
                    <HASEDDCITY>No</HASEDDCITY>
                    <HASECHEQUECITY>No</HASECHEQUECITY>
                    <ISFILENAMEFORMATSUPPORTED>No</ISFILENAMEFORMATSUPPORTED>
                    <HASCLIENTCODE>No</HASCLIENTCODE>
                    <PAYINSISBATCHAPPLICABLE>No</PAYINSISBATCHAPPLICABLE>
                    <PAYINSISFILENUMAPP>No</PAYINSISFILENUMAPP>
                    <ISSALARYTRANSGROUPEDFORBRS>No</ISSALARYTRANSGROUPEDFORBRS>
                    <ISEBANKINGSUPPORTED>No</ISEBANKINGSUPPORTED>
                    <ISSCBUAE>No</ISSCBUAE>
                    <ISBANKSTATUSAPP>No</ISBANKSTATUSAPP>
                    <ISSALARYGROUPED>No</ISSALARYGROUPED>
                    <USEFORPURCHASETAX>No</USEFORPURCHASETAX>
                    <AUDITED>No</AUDITED>
                    <SORTPOSITION> 1000</SORTPOSITION>
                    <ALTERID> 171</ALTERID>
                    <SERVICETAXDETAILS.LIST></SERVICETAXDETAILS.LIST>
                    <LBTREGNDETAILS.LIST></LBTREGNDETAILS.LIST>
                    <VATDETAILS.LIST></VATDETAILS.LIST>
                    <SALESTAXCESSDETAILS.LIST></SALESTAXCESSDETAILS.LIST>
                    <GSTDETAILS.LIST></GSTDETAILS.LIST>
                    <LANGUAGENAME.LIST>
                        <NAME.LIST TYPE="String">
                            <NAME>{ledger_name}</NAME>
                        </NAME.LIST>
                        <LANGUAGEID> 1033</LANGUAGEID>
                    </LANGUAGENAME.LIST>
                    <XBRLDETAIL.LIST></XBRLDETAIL.LIST>
                    <AUDITDETAILS.LIST></AUDITDETAILS.LIST>
                    <SCHVIDETAILS.LIST></SCHVIDETAILS.LIST>
                    <EXCISETARIFFDETAILS.LIST></EXCISETARIFFDETAILS.LIST>
                    <TCSCATEGORYDETAILS.LIST></TCSCATEGORYDETAILS.LIST>
                    <TDSCATEGORYDETAILS.LIST></TDSCATEGORYDETAILS.LIST>
                    <SLABPERIOD.LIST></SLABPERIOD.LIST>
                    <GRATUITYPERIOD.LIST></GRATUITYPERIOD.LIST>
                    <ADDITIONALCOMPUTATIONS.LIST></ADDITIONALCOMPUTATIONS.LIST>
                    <EXCISEJURISDICTIONDETAILS.LIST></EXCISEJURISDICTIONDETAILS.LIST>
                    <EXCLUDEDTAXATIONS.LIST></EXCLUDEDTAXATIONS.LIST>
                    <BANKALLOCATIONS.LIST></BANKALLOCATIONS.LIST>
                    <PAYMENTDETAILS.LIST></PAYMENTDETAILS.LIST>
                    <BANKEXPORTFORMATS.LIST></BANKEXPORTFORMATS.LIST>
                    <BILLALLOCATIONS.LIST></BILLALLOCATIONS.LIST>
                    <INTERESTCOLLECTION.LIST></INTERESTCOLLECTION.LIST>
                    <LEDGERCLOSINGVALUES.LIST></LEDGERCLOSINGVALUES.LIST>
                    <LEDGERAUDITCLASS.LIST></LEDGERAUDITCLASS.LIST>
                    <OLDAUDITENTRIES.LIST></OLDAUDITENTRIES.LIST>
                    <TDSEXEMPTIONRULES.LIST></TDSEXEMPTIONRULES.LIST>
                    <DEDUCTINSAMEVCHRULES.LIST></DEDUCTINSAMEVCHRULES.LIST>
                    <LOWERDEDUCTION.LIST></LOWERDEDUCTION.LIST>
                    <STXABATEMENTDETAILS.LIST></STXABATEMENTDETAILS.LIST>
                    <LEDMULTIADDRESSLIST.LIST></LEDMULTIADDRESSLIST.LIST>
                    <STXTAXDETAILS.LIST></STXTAXDETAILS.LIST>
                    <CHEQUERANGE.LIST></CHEQUERANGE.LIST>
                    <DEFAULTVCHCHEQUEDETAILS.LIST></DEFAULTVCHCHEQUEDETAILS.LIST>
                    <ACCOUNTAUDITENTRIES.LIST></ACCOUNTAUDITENTRIES.LIST>
                    <AUDITENTRIES.LIST></AUDITENTRIES.LIST>
                    <BRSIMPORTEDINFO.LIST></BRSIMPORTEDINFO.LIST>
                    <AUTOBRSCONFIGS.LIST></AUTOBRSCONFIGS.LIST>
                    <BANKURENTRIES.LIST></BANKURENTRIES.LIST>
                    <DEFAULTCHEQUEDETAILS.LIST></DEFAULTCHEQUEDETAILS.LIST>
                    <DEFAULTOPENINGCHEQUEDETAILS.LIST></DEFAULTOPENINGCHEQUEDETAILS.LIST>
                    <CANCELLEDPAYALLOCATIONS.LIST></CANCELLEDPAYALLOCATIONS.LIST>
                    <ECHEQUEPRINTLOCATION.LIST></ECHEQUEPRINTLOCATION.LIST>
                    <ECHEQUEPAYABLELOCATION.LIST></ECHEQUEPAYABLELOCATION.LIST>
                    <EDDPRINTLOCATION.LIST></EDDPRINTLOCATION.LIST>
                    <EDDPAYABLELOCATION.LIST></EDDPAYABLELOCATION.LIST>
                    <AVAILABLETRANSACTIONTYPES.LIST></AVAILABLETRANSACTIONTYPES.LIST>
                    <LEDPAYINSCONFIGS.LIST></LEDPAYINSCONFIGS.LIST>
                    <TYPECODEDETAILS.LIST></TYPECODEDETAILS.LIST>
                    <FIELDVALIDATIONDETAILS.LIST></FIELDVALIDATIONDETAILS.LIST>
                    <INPUTCRALLOCS.LIST></INPUTCRALLOCS.LIST>
                    <TCSMETHODOFCALCULATION.LIST></TCSMETHODOFCALCULATION.LIST>
                    <GSTCLASSFNIGSTRATES.LIST></GSTCLASSFNIGSTRATES.LIST>
                    <EXTARIFFDUTYHEADDETAILS.LIST></EXTARIFFDUTYHEADDETAILS.LIST>
                    <VOUCHERTYPEPRODUCTCODES.LIST></VOUCHERTYPEPRODUCTCODES.LIST>
                </LEDGER>
            </TALLYMESSAGE>'''


def generate_voucher(txn_date, voucher_type, narration, amount, instrument_number, alter_id=4, master_id=3):
    """
    Generate a complete Tally voucher entry
    
    Args:
        txn_date: Transaction date in YYYYMMDD format
        voucher_type: "Payment" or "Receipt"
        narration: Transaction description
        amount: Transaction amount (positive value)
        instrument_number: Reference/instrument number
        alter_id: Alter ID (default 4)
        master_id: Master ID (default 3)
    """
    
    config = load_config()
    bank_name = config['bank_account_name']
    suspense_name = config['suspense_account_name']
    transaction_type = config['default_transaction_type']
    
    # For Payment: Suspense is positive, Bank is negative
    # For Receipt: Suspense is negative, Bank is positive
    if voucher_type == "Payment":
        suspense_amount = f"-{amount:.2f}"
        bank_amount = f"{amount:.2f}"
        suspense_deemed_positive = "Yes"
        bank_deemed_positive = "No"
    else:  # Receipt
        suspense_amount = f"{amount:.2f}"
        bank_amount = f"-{amount:.2f}"
        suspense_deemed_positive = "No"
        bank_deemed_positive = "Yes"
    
    return f'''                                                                                                                                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                                <VOUCHER VCHTYPE="{voucher_type}" ACTION="Create" OBJVIEW="Accounting Voucher View">
                                    <DATE>{txn_date}</DATE>
                                    <VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>
                                    <NARRATION>{narration}</NARRATION>
                                    <PARTYLEDGERNAME>{bank_name}</PARTYLEDGERNAME>

                                    <CSTFORMISSUETYPE />
                                    <CSTFORMRECVTYPE />
                                    <FBTPAYMENTTYPE>Default</FBTPAYMENTTYPE>
                                    <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
                                    <VCHGSTCLASS />
                                    <DIFFACTUALQTY>No</DIFFACTUALQTY>
                                    <ISMSTFROMSYNC>No</ISMSTFROMSYNC>
                                    <ISDELETED>No</ISDELETED>
                                    <ISSECURITYONWHENENTERED>No</ISSECURITYONWHENENTERED>
                                    <ASORIGINAL>No</ASORIGINAL>
                                    <AUDITED>No</AUDITED>
                                    <FORJOBCOSTING>No</FORJOBCOSTING>
                                    <ISOPTIONAL>No</ISOPTIONAL>
                                    <EFFECTIVEDATE>{txn_date}</EFFECTIVEDATE>
                                    <USEFOREXCISE>No</USEFOREXCISE>
                                    <ISFORJOBWORKIN>No</ISFORJOBWORKIN>
                                    <ALLOWCONSUMPTION>No</ALLOWCONSUMPTION>
                                    <USEFORINTEREST>No</USEFORINTEREST>
                                    <USEFORGAINLOSS>No</USEFORGAINLOSS>
                                    <USEFORGODOWNTRANSFER>No</USEFORGODOWNTRANSFER>
                                    <USEFORCOMPOUND>No</USEFORCOMPOUND>
                                    <USEFORSERVICETAX>No</USEFORSERVICETAX>
                                    <ISONHOLD>No</ISONHOLD>
                                    <ISBOENOTAPPLICABLE>No</ISBOENOTAPPLICABLE>
                                    <ISGSTSECSEVENAPPLICABLE>No</ISGSTSECSEVENAPPLICABLE>
                                    <ISEXCISEVOUCHER>No</ISEXCISEVOUCHER>
                                    <EXCISETAXOVERRIDE>No</EXCISETAXOVERRIDE>
                                    <USEFORTAXUNITTRANSFER>No</USEFORTAXUNITTRANSFER>
                                    <IGNOREPOSVALIDATION>No</IGNOREPOSVALIDATION>
                                    <EXCISEOPENING>No</EXCISEOPENING>
                                    <USEFORFINALPRODUCTION>No</USEFORFINALPRODUCTION>
                                    <ISTDSOVERRIDDEN>No</ISTDSOVERRIDDEN>
                                    <ISTCSOVERRIDDEN>No</ISTCSOVERRIDDEN>
                                    <ISTDSTCSCASHVCH>No</ISTDSTCSCASHVCH>
                                    <INCLUDEADVPYMTVCH>No</INCLUDEADVPYMTVCH>
                                    <ISSUBWORKSCONTRACT>No</ISSUBWORKSCONTRACT>
                                    <ISVATOVERRIDDEN>No</ISVATOVERRIDDEN>
                                    <IGNOREORIGVCHDATE>No</IGNOREORIGVCHDATE>
                                    <ISVATPAIDATCUSTOMS>No</ISVATPAIDATCUSTOMS>
                                    <ISDECLAREDTOCUSTOMS>No</ISDECLAREDTOCUSTOMS>
                                    <ISSERVICETAXOVERRIDDEN>No</ISSERVICETAXOVERRIDDEN>
                                    <ISISDVOUCHER>No</ISISDVOUCHER>
                                    <ISEXCISEOVERRIDDEN>No</ISEXCISEOVERRIDDEN>
                                    <ISEXCISESUPPLYVCH>No</ISEXCISESUPPLYVCH>
                                    <ISGSTOVERRIDDEN>No</ISGSTOVERRIDDEN>
                                    <GSTNOTEXPORTED>No</GSTNOTEXPORTED>
                                    <IGNOREGSTINVALIDATION>No</IGNOREGSTINVALIDATION>
                                    <ISGSTREFUND>No</ISGSTREFUND>
                                    <OVRDNEWAYBILLAPPLICABILITY>No</OVRDNEWAYBILLAPPLICABILITY>
                                    <ISVATPRINCIPALACCOUNT>No</ISVATPRINCIPALACCOUNT>
                                    <IGNOREEINVVALIDATION>No</IGNOREEINVVALIDATION>
                                    <IRNJSONEXPORTED>No</IRNJSONEXPORTED>
                                    <IRNCANCELLED>No</IRNCANCELLED>
                                    <ISSHIPPINGWITHINSTATE>No</ISSHIPPINGWITHINSTATE>
                                    <ISOVERSEASTOURISTTRANS>No</ISOVERSEASTOURISTTRANS>
                                    <ISDESIGNATEDZONEPARTY>No</ISDESIGNATEDZONEPARTY>
                                    <ISCANCELLED>No</ISCANCELLED>
                                    <HASCASHFLOW>Yes</HASCASHFLOW>
                                    <ISPOSTDATED>No</ISPOSTDATED>
                                    <USETRACKINGNUMBER>No</USETRACKINGNUMBER>
                                    <ISINVOICE>No</ISINVOICE>
                                    <MFGJOURNAL>No</MFGJOURNAL>
                                    <HASDISCOUNTS>No</HASDISCOUNTS>
                                    <ASPAYSLIP>No</ASPAYSLIP>
                                    <ISCOSTCENTRE>No</ISCOSTCENTRE>
                                    <ISSTXNONREALIZEDVCH>No</ISSTXNONREALIZEDVCH>
                                    <ISEXCISEMANUFACTURERON>No</ISEXCISEMANUFACTURERON>
                                    <ISBLANKCHEQUE>No</ISBLANKCHEQUE>
                                    <ISVOID>No</ISVOID>
                                    <ORDERLINESTATUS>No</ORDERLINESTATUS>
                                    <VATISAGNSTCANCSALES>No</VATISAGNSTCANCSALES>
                                    <VATISPURCEXEMPTED>No</VATISPURCEXEMPTED>
                                    <ISVATRESTAXINVOICE>No</ISVATRESTAXINVOICE>
                                    <VATISASSESABLECALCVCH>No</VATISASSESABLECALCVCH>
                                    <ISVATDUTYPAID>Yes</ISVATDUTYPAID>
                                    <ISDELIVERYSAMEASCONSIGNEE>No</ISDELIVERYSAMEASCONSIGNEE>
                                    <ISDISPATCHSAMEASCONSIGNOR>No</ISDISPATCHSAMEASCONSIGNOR>
                                    <ISDELETEDVCHRETAINED>No</ISDELETEDVCHRETAINED>
                                    <CHANGEVCHMODE>No</CHANGEVCHMODE>
                                    <RESETIRNQRCODE>No</RESETIRNQRCODE>
                                    <ALTERID> {alter_id}</ALTERID>
                                    <MASTERID> {master_id}</MASTERID>
                                    <EWAYBILLDETAILS.LIST></EWAYBILLDETAILS.LIST>
                                    <EXCLUDEDTAXATIONS.LIST></EXCLUDEDTAXATIONS.LIST>
                                    <OLDAUDITENTRIES.LIST></OLDAUDITENTRIES.LIST>
                                    <ACCOUNTAUDITENTRIES.LIST></ACCOUNTAUDITENTRIES.LIST>
                                    <AUDITENTRIES.LIST></AUDITENTRIES.LIST>
                                    <DUTYHEADDETAILS.LIST></DUTYHEADDETAILS.LIST>
                                    <SUPPLEMENTARYDUTYHEADDETAILS.LIST></SUPPLEMENTARYDUTYHEADDETAILS.LIST>
                                    <EWAYBILLERRORLIST.LIST></EWAYBILLERRORLIST.LIST>
                                    <IRNERRORLIST.LIST></IRNERRORLIST.LIST>
                                    <INVOICEDELNOTES.LIST></INVOICEDELNOTES.LIST>
                                    <INVOICEORDERLIST.LIST></INVOICEORDERLIST.LIST>
                                    <INVOICEINDENTLIST.LIST></INVOICEINDENTLIST.LIST>
                                    <ATTENDANCEENTRIES.LIST></ATTENDANCEENTRIES.LIST>
                                    <ORIGINVOICEDETAILS.LIST></ORIGINVOICEDETAILS.LIST>
                                    <INVOICEEXPORTLIST.LIST></INVOICEEXPORTLIST.LIST>
                                    <ALLLEDGERENTRIES.LIST>
                                        <LEDGERNAME>{suspense_name}</LEDGERNAME>
                                        <GSTCLASS />
                                        <ISDEEMEDPOSITIVE>{suspense_deemed_positive}</ISDEEMEDPOSITIVE>
                                        <LEDGERFROMITEM>No</LEDGERFROMITEM>
                                        <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
                                        <ISPARTYLEDGER>No</ISPARTYLEDGER>
                                        <ISLASTDEEMEDPOSITIVE>{suspense_deemed_positive}</ISLASTDEEMEDPOSITIVE>
                                        <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
                                        <ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED>
                                        <AMOUNT>{suspense_amount}</AMOUNT>
                                        <SERVICETAXDETAILS.LIST></SERVICETAXDETAILS.LIST>
                                        <BANKALLOCATIONS.LIST></BANKALLOCATIONS.LIST>
                                        <BILLALLOCATIONS.LIST></BILLALLOCATIONS.LIST>
                                        <INTERESTCOLLECTION.LIST></INTERESTCOLLECTION.LIST>
                                        <OLDAUDITENTRIES.LIST></OLDAUDITENTRIES.LIST>
                                        <ACCOUNTAUDITENTRIES.LIST></ACCOUNTAUDITENTRIES.LIST>
                                        <AUDITENTRIES.LIST></AUDITENTRIES.LIST>
                                        <INPUTCRALLOCS.LIST></INPUTCRALLOCS.LIST>
                                        <DUTYHEADDETAILS.LIST></DUTYHEADDETAILS.LIST>
                                        <EXCISEDUTYHEADDETAILS.LIST></EXCISEDUTYHEADDETAILS.LIST>
                                        <RATEDETAILS.LIST></RATEDETAILS.LIST>
                                        <SUMMARYALLOCS.LIST></SUMMARYALLOCS.LIST>
                                        <STPYMTDETAILS.LIST></STPYMTDETAILS.LIST>
                                        <EXCISEPAYMENTALLOCATIONS.LIST></EXCISEPAYMENTALLOCATIONS.LIST>
                                        <TAXBILLALLOCATIONS.LIST></TAXBILLALLOCATIONS.LIST>
                                        <TAXOBJECTALLOCATIONS.LIST></TAXOBJECTALLOCATIONS.LIST>
                                        <TDSEXPENSEALLOCATIONS.LIST></TDSEXPENSEALLOCATIONS.LIST>
                                        <VATSTATUTORYDETAILS.LIST></VATSTATUTORYDETAILS.LIST>
                                        <COSTTRACKALLOCATIONS.LIST></COSTTRACKALLOCATIONS.LIST>
                                        <REFVOUCHERDETAILS.LIST></REFVOUCHERDETAILS.LIST>
                                        <INVOICEWISEDETAILS.LIST></INVOICEWISEDETAILS.LIST>
                                        <VATITCDETAILS.LIST></VATITCDETAILS.LIST>
                                        <ADVANCETAXDETAILS.LIST></ADVANCETAXDETAILS.LIST>
                                    </ALLLEDGERENTRIES.LIST>
                                    <ALLLEDGERENTRIES.LIST>
                                        <LEDGERNAME>{bank_name}</LEDGERNAME>
                                        <GSTCLASS />
                                        <ISDEEMEDPOSITIVE>{bank_deemed_positive}</ISDEEMEDPOSITIVE>
                                        <LEDGERFROMITEM>No</LEDGERFROMITEM>
                                        <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
                                        <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
                                        <ISLASTDEEMEDPOSITIVE>{bank_deemed_positive}</ISLASTDEEMEDPOSITIVE>
                                        <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
                                        <ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED>
                                        <AMOUNT>{bank_amount}</AMOUNT>
                                        <SERVICETAXDETAILS.LIST></SERVICETAXDETAILS.LIST>
                                        <BANKALLOCATIONS.LIST>
                                            <DATE>{txn_date}</DATE>
                                            <INSTRUMENTDATE>{txn_date}</INSTRUMENTDATE>
                                            <PAYMENTFAVOURING>{suspense_name}</PAYMENTFAVOURING>
                                            <TRANSACTIONTYPE>{transaction_type}</TRANSACTIONTYPE>
                                                                                            <INSTRUMENTNUMBER>{instrument_number}</INSTRUMENTNUMBER>
                                                                                        <STATUS>No</STATUS>
                                            <PAYMENTMODE>Transacted</PAYMENTMODE>
                                            <BANKPARTYNAME>{suspense_name}</BANKPARTYNAME>
                                            <ISCONNECTEDPAYMENT>No</ISCONNECTEDPAYMENT>
                                            <ISSPLIT>No</ISSPLIT>
                                            <ISCONTRACTUSED>No</ISCONTRACTUSED>
                                            <ISACCEPTEDWITHWARNING>No</ISACCEPTEDWITHWARNING>
                                            <ISTRANSFORCED>No</ISTRANSFORCED>
                                            <AMOUNT>{bank_amount}</AMOUNT>
                                            <CONTRACTDETAILS.LIST></CONTRACTDETAILS.LIST>
                                            <BANKSTATUSINFO.LIST></BANKSTATUSINFO.LIST>
                                        </BANKALLOCATIONS.LIST>
                                        <BILLALLOCATIONS.LIST></BILLALLOCATIONS.LIST>
                                        <INTERESTCOLLECTION.LIST></INTERESTCOLLECTION.LIST>
                                        <OLDAUDITENTRIES.LIST></OLDAUDITENTRIES.LIST>
                                        <ACCOUNTAUDITENTRIES.LIST></ACCOUNTAUDITENTRIES.LIST>
                                        <AUDITENTRIES.LIST></AUDITENTRIES.LIST>
                                        <INPUTCRALLOCS.LIST></INPUTCRALLOCS.LIST>
                                        <DUTYHEADDETAILS.LIST></DUTYHEADDETAILS.LIST>
                                        <EXCISEDUTYHEADDETAILS.LIST></EXCISEDUTYHEADDETAILS.LIST>
                                        <RATEDETAILS.LIST></RATEDETAILS.LIST>
                                        <SUMMARYALLOCS.LIST></SUMMARYALLOCS.LIST>
                                        <STPYMTDETAILS.LIST></STPYMTDETAILS.LIST>
                                        <EXCISEPAYMENTALLOCATIONS.LIST></EXCISEPAYMENTALLOCATIONS.LIST>
                                        <TAXBILLALLOCATIONS.LIST></TAXBILLALLOCATIONS.LIST>
                                        <TAXOBJECTALLOCATIONS.LIST></TAXOBJECTALLOCATIONS.LIST>
                                        <TDSEXPENSEALLOCATIONS.LIST></TDSEXPENSEALLOCATIONS.LIST>
                                        <VATSTATUTORYDETAILS.LIST></VATSTATUTORYDETAILS.LIST>
                                        <COSTTRACKALLOCATIONS.LIST></COSTTRACKALLOCATIONS.LIST>
                                        <REFVOUCHERDETAILS.LIST></REFVOUCHERDETAILS.LIST>
                                        <INVOICEWISEDETAILS.LIST></INVOICEWISEDETAILS.LIST>
                                        <VATITCDETAILS.LIST></VATITCDETAILS.LIST>
                                        <ADVANCETAXDETAILS.LIST></ADVANCETAXDETAILS.LIST>
                                    </ALLLEDGERENTRIES.LIST>
                                    <PAYROLLMODEOFPAYMENT.LIST></PAYROLLMODEOFPAYMENT.LIST>
                                    <ATTDRECORDS.LIST></ATTDRECORDS.LIST>
                                    <GSTEWAYCONSIGNORADDRESS.LIST></GSTEWAYCONSIGNORADDRESS.LIST>
                                    <GSTEWAYCONSIGNEEADDRESS.LIST></GSTEWAYCONSIGNEEADDRESS.LIST>
                                    <TEMPGSTRATEDETAILS.LIST></TEMPGSTRATEDETAILS.LIST>
                                </VOUCHER>
                            </TALLYMESSAGE>'''


def get_xml_footer():
    """Generate XML footer closing tags"""
    return '''                                                                                </REQUESTDATA>
    </IMPORTDATA>
</BODY>
</ENVELOPE>
'''
