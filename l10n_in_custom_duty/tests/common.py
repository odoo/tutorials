from odoo.tests.common import TransactionCase
from odoo import fields, Command


class Common(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.currency_inr = cls.env["res.currency"].create({
            "name": "ABC",
            "symbol": "₹",
            "decimal_places": 2
        })

        cls.currency_usd = cls.env["res.currency"].create({
            "name": "XYZ",
            "symbol": "$",
            "decimal_places": 2
        })

        cls.company_india = cls.env["res.company"].create({
            "name": "Test Company India",
            "country_id": cls.env.ref("base.in").id,
            "currency_id": cls.currency_inr.id
        })

        cls.payable_account = cls.env["account.account"].create({
            "name": "Accounts Payable",
            "code": "100001",
            "account_type": "liability_payable",
            "company_ids": [Command.link(cls.company_india.id)]
        })

        cls.vendor_partner = cls.env["res.partner"].create({
            "name": "Test Vendor",
            "company_id": cls.company_india.id,
            "country_id": cls.env.ref("base.us").id
        })

        cls.purchase_expense_account = cls.env["account.account"].create({
            "name": "Purchase Expense Account",
            "code": "200001",
            "account_type": "expense",
            "company_ids": [Command.link(cls.company_india.id)]
        })

        cls.purchase_journal = cls.env["account.journal"].create({
            "name": "Purchase Journal",
            "code": "PUR",
            "company_id": cls.company_india.id,
            "type": "purchase",
            "default_account_id": cls.purchase_expense_account.id
        })
        
        cls.tax_group_igst = cls.env["account.tax.group"].create({"name": "IGST", "company_id": cls.company_india.id})

        cls.tax_account = cls.env["account.account"].create({
            "name": "Tax Account",
            "code": "100100",
            "account_type": "liability_current",
            "company_ids": [Command.link(cls.company_india.id)],
            "reconcile": True
        })

        cls.igst_tax_5 = cls.env["account.tax"].create({
            "name": "IGST 5%",
            "amount": 5.0,
            "amount_type": "percent",
            "type_tax_use": "purchase",
            "company_id": cls.company_india.id,
            "tax_group_id": cls.tax_group_igst.id,
            "invoice_repartition_line_ids": [
                Command.create({"repartition_type": "base"}),
                Command.create({"factor_percent": 100, "repartition_type": "tax", "account_id": cls.tax_account.id})
            ]
        })

        cls.igst_tax_12 = cls.env["account.tax"].create({
            "name": "IGST 12%",
            "amount": 12.0,
            "amount_type": "percent",
            "type_tax_use": "purchase",
            "company_id": cls.company_india.id,
            "tax_group_id": cls.tax_group_igst.id,
            "invoice_repartition_line_ids": [
                Command.create({"repartition_type": "base"}),
                Command.create({"factor_percent": 100, "repartition_type": "tax", "account_id": cls.tax_account.id})
            ]
        })
        
        cls.import_custom_duty_account = cls.env["account.account"].create({
            "name": "Import Custom Duty Account",
            "code": "200002",
            "account_type": "expense",
            "company_ids": [Command.link(cls.company_india.id)]
        })

        cls.import_default_tax_account = cls.env["account.account"].create({
            "name": "Import Default Tax Account",
            "code": "100200",
            "account_type": "liability_current",
            "company_ids": [Command.link(cls.company_india.id)],
            "reconcile": True
        })

        cls.import_journal = cls.env["account.journal"].create({
            "name": "Import Journal",
            "code": "IMP",
            "company_id": cls.company_india.id,
            "type": "general"
        })

        cls.company_india.write({
            "import_custom_duty_journal_id": cls.import_journal.id,
            "import_custom_duty_account_id": cls.import_custom_duty_account.id,
            "import_default_tax_account_id": cls.import_default_tax_account.id
        })
        
        cls.env.user.company_id = cls.company_india
        cls.env.company = cls.company_india
    
    def setUp(self):
        super().setUp()
        
        self.vendor_bill = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.vendor_partner.id,
            "currency_id": self.currency_usd.id,
            "company_id": self.company_india.id,
            "invoice_date": fields.Date.today(),
            "bill_of_entry_custom_currency_rate": 82.36,
            "invoice_line_ids": [
                Command.create({
                    "name": "Test Expense",
                    "account_id": self.purchase_expense_account.id,
                    "price_unit": 100,
                    "quantity": 1,
                }),
                Command.create({
                    "name": "Another Test Expense",
                    "account_id": self.purchase_expense_account.id,
                    "price_unit": 100,
                    "quantity": 3,
                })
            ]
        })
        self.vendor_bill.action_post()        
        self.custom_duty_wizard = self.env["account.move.custom.duty"].with_context(active_id=self.vendor_bill.id).create({})
