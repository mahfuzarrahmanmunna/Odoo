import os

Company = env['res.company'].sudo()
companies = Company.search([])

if len(companies) != 1:
    raise Exception("Exactly one company is required.")

company = companies[0]

if company.country_id.code != 'BD':
    raise Exception("Set company country to Bangladesh first.")

if company.currency_id.name != 'BDT':
    raise Exception("Set company currency to BDT first.")

Account = env['account.account'].sudo().with_company(company)

accounts = [

    # ==========================================
    # ASSETS
    # ==========================================

    ('100001', 'Liquidity Transfer', 'asset_current', True),
    ('101001', 'Bank Account', 'asset_cash', False),
    ('101002', 'Bank Suspense Account', 'asset_current', True),
    ('101003', 'Outstanding Receipts', 'asset_current', True),
    ('101004', 'Outstanding Payments', 'asset_current', True),

    ('101011', 'bKash Merchant Account', 'asset_cash', False),
    ('101012', 'Nagad Merchant Account', 'asset_cash', False),
    ('101013', 'Rocket Merchant Account', 'asset_cash', False),
    ('101014', 'Card Payment Clearing', 'asset_current', True),
    ('101015', 'Online Payment Gateway Clearing', 'asset_current', True),
    ('101016', 'Mobile Banking Settlement Clearing', 'asset_current', True),

    ('102011', 'Accounts Receivable', 'asset_receivable', True),
    ('102012', 'Accounts Receivable - POS', 'asset_receivable', True),
    ('102013', 'Post Dated Cheques Received', 'asset_current', True),
    ('102014', 'Other Receivables', 'asset_current', True),
    ('102015', 'Employee Advance', 'asset_current', True),
    ('102016', 'Supplier Advance', 'asset_current', True),

    # Inventory

    ('103001', 'Merchandise Inventory', 'asset_current', False),
    ('103002', 'Stock Interim Received', 'asset_current', True),
    ('103003', 'Stock Interim Delivered', 'asset_current', True),
    ('103004', 'Goods in Transit', 'asset_current', False),
    ('103005', 'Packaging Materials Inventory', 'asset_current', False),
    ('103006', 'Inventory Landed Cost Clearing', 'asset_current', True),

    # Prepayments and Tax Assets

    ('104020', 'Prepaid Expenses', 'asset_prepayments', False),
    ('104023', 'Prepaid Showroom Rent', 'asset_prepayments', False),
    ('104024', 'Prepaid Insurance', 'asset_prepayments', False),
    ('104025', 'Prepaid License Fees', 'asset_prepayments', False),
    ('104026', 'Prepaid Maintenance', 'asset_prepayments', False),
    ('104027', 'Prepaid Software Subscription', 'asset_prepayments', False),
    ('104033', 'Prepaid Advertising', 'asset_prepayments', False),
    ('104037', 'Showroom Security Deposit', 'asset_non_current', False),
    ('104040', 'Other Security Deposits', 'asset_non_current', False),
    ('104041', 'Input VAT Receivable', 'asset_current', False),
    ('104042', 'Advance Income Tax - AIT', 'asset_current', False),
    ('104043', 'Tax Deducted at Source Receivable', 'asset_current', False),
    ('104044', 'VAT Deducted at Source Receivable', 'asset_current', False),

    # Cash

    ('105001', 'Cash in Hand', 'asset_cash', False),
    ('105002', 'POS Cash', 'asset_cash', False),
    ('105004', 'Petty Cash', 'asset_cash', False),

    # Fixed Assets

    ('106001', 'Leasehold Improvements', 'asset_fixed', False),
    ('106002', 'Furniture and Fixtures', 'asset_fixed', False),
    ('106003', 'Computer and POS Equipment', 'asset_fixed', False),
    ('106004', 'Motor Vehicles', 'asset_fixed', False),
    ('106005', 'Capital Work in Progress', 'asset_non_current', False),
    ('106006', 'Accumulated Depreciation - Leasehold Improvements', 'asset_fixed', False),
    ('106007', 'Accumulated Depreciation - Furniture', 'asset_fixed', False),
    ('106008', 'Accumulated Depreciation - Computers', 'asset_fixed', False),
    ('106009', 'Accumulated Depreciation - Vehicles', 'asset_fixed', False),
    ('106010', 'Trademark and Software Rights', 'asset_non_current', False),
    ('106012', 'Display Racks and Shelving', 'asset_fixed', False),
    ('106013', 'Lighting and Electrical Equipment', 'asset_fixed', False),
    ('106014', 'Air Conditioner and Appliances', 'asset_fixed', False),
    ('106015', 'CCTV and Security Equipment', 'asset_fixed', False),
    ('106016', 'Accumulated Depreciation - Display Racks', 'asset_fixed', False),
    ('106017', 'Accumulated Depreciation - Electrical Equipment', 'asset_fixed', False),
    ('106018', 'Accumulated Depreciation - Appliances', 'asset_fixed', False),
    ('106019', 'Accumulated Depreciation - Security Equipment', 'asset_fixed', False),

    # ==========================================
    # LIABILITIES
    # ==========================================

    ('201002', 'Accounts Payable', 'liability_payable', True),
    ('201003', 'Customer Advance', 'liability_current', True),
    ('201004', 'Salary Payable', 'liability_current', True),
    ('201006', 'Leave Salary Payable', 'liability_current', False),
    ('201007', 'Sales Commission Payable', 'liability_current', False),
    ('201009', 'Festival Bonus Payable', 'liability_current', False),
    ('201011', 'Utilities Payable', 'liability_current', False),
    ('201012', 'Telephone and Internet Payable', 'liability_current', False),
    ('201014', 'Audit Fees Payable', 'liability_current', False),
    ('201015', 'Showroom Rent Payable', 'liability_current', False),
    ('201016', 'Other Accrued Expenses', 'liability_current', False),
    ('201017', 'Output VAT Payable', 'liability_current', False),
    ('201018', 'Deferred Income', 'liability_current', False),
    ('201020', 'TDS Payable', 'liability_current', False),
    ('201021', 'VDS Payable', 'liability_current', False),
    ('201022', 'VAT Settlement Payable', 'liability_current', False),
    ('201023', 'Income Tax Payable', 'liability_current', False),
    ('201024', 'Short Term Bank Loan', 'liability_current', False),
    ('201025', 'Bank Overdraft', 'liability_current', False),
    ('201026', 'Gift Voucher Liability', 'liability_current', False),
    ('201027', 'Customer Refund Payable', 'liability_current', True),
    ('201028', 'Current Portion of Long Term Loan', 'liability_current', False),

    ('202001', 'Gratuity Provision', 'liability_non_current', False),
    ('202004', 'Long Term Bank Loan', 'liability_non_current', False),
    ('202005', 'Long Term Lease Liability', 'liability_non_current', False),

    # ==========================================
    # EQUITY
    # ==========================================

    ('301001', 'Owners Capital', 'equity', False),
    ('301002', 'Additional Capital Contribution', 'equity', False),
    ('301003', 'Owners Drawings', 'equity', False),
    ('301004', 'Retained Earnings', 'equity', False),
    ('301005', 'General Reserve', 'equity', False),

    # ==========================================
    # COST OF GOODS SOLD
    # ==========================================

    ('400001', 'Cost of Goods Sold', 'expense_direct_cost', False),
    ('410001', 'Purchase Freight and Transportation', 'expense_direct_cost', False),
    ('410002', 'Non Recoverable Import Duty', 'expense_direct_cost', False),
    ('410003', 'Purchase Handling Charges', 'expense_direct_cost', False),
    ('410004', 'Inventory Shrinkage and Damage', 'expense_direct_cost', False),
    ('410005', 'Inventory Valuation Adjustment', 'expense_direct_cost', False),
    ('410006', 'Purchase Price Difference', 'expense_direct_cost', False),

    # ==========================================
    # OPERATING EXPENSES
    # ==========================================

    ('400003', 'Basic Salary', 'expense', False),
    ('400004', 'House Rent Allowance', 'expense', False),
    ('400005', 'Conveyance Allowance', 'expense', False),
    ('400007', 'Leave Salary Expense', 'expense', False),
    ('400009', 'Medical Allowance', 'expense', False),
    ('400011', 'Sales Commission', 'expense', False),
    ('400012', 'Other Staff Allowances', 'expense', False),
    ('400013', 'Staff Uniform Expense', 'expense', False),
    ('400015', 'Other Personnel Expenses', 'expense', False),
    ('400016', 'Showroom Rent', 'expense', False),
    ('400017', 'Storage Rent', 'expense', False),
    ('400018', 'Electricity and Water Bill', 'expense', False),
    ('400019', 'Other Utility Expenses', 'expense', False),
    ('400020', 'Telephone and Internet', 'expense', False),
    ('400021', 'Courier and Delivery Charges', 'expense', False),
    ('400022', 'Website and Hosting Expense', 'expense', False),
    ('400026', 'Staff Meals and Refreshments', 'expense', False),
    ('400029', 'Audit and Accounting Fees', 'expense', False),
    ('400031', 'Legal Expenses', 'expense', False),
    ('400032', 'Trade License and Renewal Fees', 'expense', False),
    ('400033', 'Professional Fees', 'expense', False),
    ('400034', 'Advertising and Marketing', 'expense', False),
    ('400035', 'Bad Debt Expense', 'expense', False),
    ('400038', 'Cash Shortage', 'expense', False),
    ('400040', 'Insurance Expense', 'expense', False),
    ('400041', 'Staff Training', 'expense', False),
    ('400042', 'Repair and Maintenance', 'expense', False),
    ('400043', 'Security and Guard Expense', 'expense', False),
    ('400044', 'Cleaning Expense', 'expense', False),
    ('400045', 'Software Subscription Expense', 'expense', False),
    ('400046', 'Gifts and Donations', 'expense', False),
    ('400048', 'Vehicle Expense', 'expense', False),
    ('400049', 'Local Conveyance Expense', 'expense', False),
    ('400050', 'Office and Stationery Expense', 'expense', False),
    ('400051', 'Bank Charges', 'expense', False),
    ('400052', 'Loss on Asset Disposal', 'expense', False),
    ('400053', 'Foreign Exchange Loss', 'expense', False),
    ('400055', 'Income Tax Expense', 'expense', False),
    ('400057', 'Other Operating Expenses', 'expense', False),
    ('400058', 'Card Processing Charges', 'expense', False),
    ('400059', 'Loan Interest and Finance Charges', 'expense', False),
    ('400063', 'Depreciation - Leasehold Improvements', 'expense_depreciation', False),
    ('400064', 'Depreciation - Furniture', 'expense_depreciation', False),
    ('400065', 'Depreciation - Computer and POS Equipment', 'expense_depreciation', False),
    ('400066', 'Depreciation - Motor Vehicles', 'expense_depreciation', False),
    ('400067', 'Consultancy Fees', 'expense', False),
    ('400068', 'Doubtful Debt Expense', 'expense', False),

    ('420001', 'Festival Bonus Expense', 'expense', False),
    ('420002', 'Overtime Expense', 'expense', False),
    ('420003', 'Staff Incentive Expense', 'expense', False),
    ('420004', 'Gratuity Expense', 'expense', False),
    ('420005', 'Shopping Bag and Packaging Expense', 'expense', False),
    ('420006', 'bKash Transaction Charges', 'expense', False),
    ('420007', 'Nagad Transaction Charges', 'expense', False),
    ('420008', 'Rocket Transaction Charges', 'expense', False),
    ('420009', 'Payment Gateway Charges', 'expense', False),
    ('420010', 'POS and Barcode Supplies', 'expense', False),
    ('420011', 'Showroom Decoration Expense', 'expense', False),
    ('420012', 'Depreciation - Display Racks', 'expense_depreciation', False),
    ('420013', 'Depreciation - Electrical Equipment', 'expense_depreciation', False),
    ('420014', 'Depreciation - Appliances', 'expense_depreciation', False),
    ('420015', 'Depreciation - Security Equipment', 'expense_depreciation', False),

    # ==========================================
    # REVENUE
    # ==========================================

    ('500001', 'Retail Sales', 'income', False),
    ('500014', 'Wholesale Sales', 'income', False),
    ('500015', 'Online Sales', 'income', False),
    ('500016', 'Sales Returns and Allowances', 'income', False),
    ('500017', 'Sales Discounts', 'income', False),
    ('500008', 'Service Income', 'income', False),
    ('500009', 'Bank Interest Income', 'income_other', False),
    ('500010', 'Gain on Asset Disposal', 'income_other', False),
    ('500011', 'Foreign Exchange Gain', 'income_other', False),
    ('500013', 'Other Income', 'income_other', False),

    # ==========================================
    # SYSTEM ACCOUNTS
    # ==========================================

    ('999001', 'Cash Difference Gain', 'income_other', False),
    ('999002', 'Cash Difference Loss', 'expense', False),
    ('999997', 'Cash Discount Gain', 'income_other', False),
    ('999998', 'Cash Discount Loss', 'expense', False),
    ('999999', 'Current Year Earnings', 'equity_unaffected', False),

]

apply_changes = os.getenv('COA_APPLY') == '1'

created = 0
skipped = 0
conflicts = 0

for code, name, account_type, reconcile in accounts:

    existing = Account.search([
        ('code', '=', code),
        ('company_id', '=', company.id),
    ], limit=1)

    if existing:
        if existing.name != name or existing.account_type != account_type:
            print(f"CONFLICT: {code} | Existing: {existing.name} | Proposed: {name}")
            conflicts += 1
        else:
            print(f"EXISTS: {code} - {existing.name}")
            skipped += 1
        continue

    if account_type == 'equity_unaffected':
        existing_earnings = Account.search([
            ('company_id', '=', company.id),
            ('account_type', '=', 'equity_unaffected'),
        ], limit=1)

        if existing_earnings:
            print(f"SKIPPED: Existing earnings account {existing_earnings.code}")
            skipped += 1
            continue

    same_name = Account.search([
        ('company_id', '=', company.id),
        ('name', '=ilike', name),
    ], limit=1)

    if same_name:
        print(f"REVIEW DUPLICATE: {code} - {name} already exists as {same_name.code}")
        conflicts += 1
        continue

    if apply_changes:
        Account.create({
            'code': code,
            'name': name,
            'account_type': account_type,
            'reconcile': reconcile,
            'company_id': company.id,
        })

    created += 1
    print(f"{'CREATED' if apply_changes else 'PREVIEW'}: {code} - {name}")

print("=" * 60)
print("BANGLADESH RETAIL CHART OF ACCOUNTS")
print("Company:", company.name)
print("Country:", company.country_id.name)
print("Currency:", company.currency_id.name)
print("Proposed accounts:", len(accounts))
print("New accounts:", created)
print("Existing/skipped:", skipped)
print("Conflicts requiring review:", conflicts)

if apply_changes:
    env.cr.commit()
    print("CHART OF ACCOUNTS SAVED")
else:
    env.cr.rollback()
    print("PREVIEW ONLY - NO CHANGES SAVED")

print("=" * 60)

