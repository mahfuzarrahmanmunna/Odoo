import os

APPLY = os.getenv('BD_APPLY') == '1'

companies = env['res.company'].sudo().search([])

if len(companies) != 1:
    raise Exception("Exactly one company required.")

company = companies[0]

if company.country_id.code != 'BD':
    raise Exception("Company must be Bangladesh.")

if company.currency_id.name != 'BDT':
    raise Exception("Company currency must be BDT.")

domain = [('company_id', '=', company.id)]

if env['account.move'].sudo().search_count(domain):
    raise Exception("Existing accounting entries found.")

sessions = env['pos.session'].sudo().search(
    domain + [('state', '!=', 'closed')]
)

if sessions:
    raise Exception("Close all POS sessions first.")

Account = env['account.account'].sudo().with_company(company)
Journal = env['account.journal'].sudo().with_company(company)

def get_account(code):
    account = Account.search(
        domain + [('code', '=', code)],
        limit=1
    )

    if not account:
        raise Exception(f"Missing account: {code}")

    if account.deprecated:
        raise Exception(f"Deprecated account: {code}")

    return account

journals = [
    ('INV', 'Customer Invoices', 'sale', '500001'),
    ('BILL', 'Vendor Bills', 'purchase', '500000'),
    ('BNK1', 'Bank Account', 'bank', '101001'),
    ('CSH1', 'Cash in Hand', 'cash', '105001'),
    ('POSC', 'POS Cash', 'cash', '105002'),
    ('PET', 'Petty Cash', 'cash', '105004'),
    ('BKSH', 'bKash Merchant', 'bank', '101011'),
    ('NGD', 'Nagad Merchant', 'bank', '101012'),
    ('RKT', 'Rocket Merchant', 'bank', '101013'),
    ('PAY', 'Salary and Payroll', 'general', None),
    ('EXP', 'Expense Management', 'general', None),
]

print("=" * 65)
print("BANGLADESH JOURNAL CONFIGURATION")
print("=" * 65)

for code, name, journal_type, account_code in journals:

    journal = Journal.search(
        domain + [('code', '=', code)],
        limit=1
    )

    values = {
        'name': name,
        'code': code,
        'type': journal_type,
        'company_id': company.id,
    }

    if account_code:
        account = get_account(account_code)

        if journal_type in ('bank', 'cash'):
            if account.account_type != 'asset_cash':
                raise Exception(
                    f"Invalid liquidity account: {account_code}"
                )

            other = Journal.search(
                domain + [
                    ('default_account_id', '=', account.id),
                    ('id', '!=', journal.id or 0)
                ],
                limit=1
            )

            if other:
                raise Exception(
                    f"{account_code} already used by {other.name}"
                )

        values['default_account_id'] = account.id

    if journal:
        if journal.type != journal_type:
            raise Exception(f"Journal type conflict: {code}")

        update_values = {
            key: value
            for key, value in values.items()
            if key not in ('type', 'company_id', 'code')
        }

        if APPLY:
            journal.write(update_values)

        print(f"UPDATE: {code} | {name} | {account_code}")

    else:
        if APPLY:
            Journal.create(values)

        print(f"CREATE: {code} | {name} | {account_code}")

if APPLY:
    env.cr.commit()
    print("JOURNAL CONFIGURATION SAVED")
else:
    env.cr.rollback()
    print("PREVIEW ONLY - NO CHANGES SAVED")

print("=" * 65)

