from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BillOfEntry(models.Model):
    _name = "bill.of.entry"
    _description = "Bill of Entry"

    account_move_id = fields.Many2one("account.move")
    currency_id = fields.Many2one(
        comodel_name="res.currency", compute="_compute_currency_id"
    )
    custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",default=1
    )
    journal_entry_number = fields.Integer(string="Journal Entry Number")
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal")
    journal_entry_date = fields.Date(
        default=fields.Date.today(), string="Journal Entry Date"
    )
    bill_of_entry_number = fields.Char(
        string="Bill of Entry No.",
        related="account_move_id.l10n_in_shipping_bill_number",
        readonly=False,
    )
    bill_of_entry_date = fields.Date(
        string="Bill of Entry Date",
        related="account_move_id.l10n_in_shipping_bill_date",
        readonly=False,
    )
    port_code_id = fields.Many2one(
        comodel_name="l10n_in.port.code",
        string="Port Code",
        related="account_move_id.l10n_in_shipping_port_code_id",
        readonly=False,
    )
    bill_of_entry_line_ids = fields.One2many(
        comodel_name="bill.of.entry.line",
        inverse_name="bill_of_entry_id",
        help="Joins the bill of entry wizard to bill of entry line wizard",
    )
    tot_custom_duty_additional_charge = fields.Monetary(
        string="Total Custom duty + Additional Charge",
        compute="_compute_total_custom_charge",
        store=True,
    )
    total_tax_amount = fields.Monetary(
        string="Total Tax Amount", compute="_compute_total_tax_amount", store=True
    )
    total_amount_payable = fields.Monetary(
        string="Total Amount Payable",
        compute="_compute_total_amount_payable",
        store=True,
    )
    is_confirmed_boe = fields.Boolean(related="account_move_id.is_confirmed_boe")
    custom_journal_entry_id = fields.Many2one(
        comodel_name="account.move", related="account_move_id.custom_journal_entry_id"
    )
    custom_journal_entry_line_ids = fields.One2many(
        related="account_move_id.custom_journal_entry_id.line_ids"
    )
    country_id=fields.Many2one(comodel_name="res.country",required=True,)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        account_move_id = self.env.context.get("default_move_id")
        account_move = self.env["account.move"].browse(account_move_id)
        res["account_move_id"] = account_move.id
        res["journal_id"] = account_move.company_id.import_journal_id.id
        res["journal_entry_number"] = account_move.company_id.import_journal_id.sequence
        return res

    @api.onchange("custom_currency_rate")
    def onchange_bill_of_entry_line(self):
        if self.bill_of_entry_line_ids:
            for line in self.bill_of_entry_line_ids:
                for move_line in self.account_move_id.line_ids.filtered(lambda l: l.product_id):
                    line.assessable_value = move_line.price_subtotal * self.custom_currency_rate

        else:
            lines = []
            for move_line in self.account_move_id.line_ids.filtered(lambda l: l.product_id):
                assessable_value = move_line.price_subtotal * self.custom_currency_rate
                print(move_line.product_id)
                lines.append(
                    (
                        0,
                        0,
                        {
                            "bill_of_entry_id": self.id,
                            "product_id": move_line.product_id,
                            "price_subtotal": move_line.price_subtotal,
                            "assessable_value": assessable_value,
                        },
                    )
                )
            self.bill_of_entry_line_ids = lines

    @api.depends("bill_of_entry_line_ids.custom_duty_additional_charge")
    def _compute_total_custom_charge(self):
        for rec in self:
            rec.tot_custom_duty_additional_charge = sum(
                rec.bill_of_entry_line_ids.mapped("custom_duty_additional_charge")
            )

    @api.depends("bill_of_entry_line_ids.tax_amount")
    def _compute_total_tax_amount(self):
        for rec in self:
            rec.total_tax_amount = sum(rec.bill_of_entry_line_ids.mapped("tax_amount"))

    @api.depends("total_tax_amount", "tot_custom_duty_additional_charge")
    def _compute_total_amount_payable(self):
        for rec in self:
            rec.total_amount_payable = (
                rec.total_tax_amount + rec.tot_custom_duty_additional_charge
            )

    @api.depends("account_move_id.company_id")
    def _compute_currency_id(self):
        for rec in self:
            rec.currency_id = self.env["res.currency"].search(
                [("name", "=", "INR")], limit=1
            )

    def action_confirm_boe(self):
        self.ensure_one()
        self.account_move_id.is_confirmed_boe = True
        if self.custom_journal_entry_id:
            return
        if (
            not self.journal_id
            or not self.account_move_id.company_id.import_custom_duty_account_id
            or not self.account_move_id.company_id.import_default_tax_account_id
        ):
            raise ValidationError("Please set import journal and accounts!")

        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": self.journal_entry_date,
                "journal_id": self.journal_id.id,
                "ref": self.account_move_id.name,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Total Custom Duty Additional Charges",
                            "account_id": self.account_move_id.company_id.import_custom_duty_account_id.id,
                            "debit": self.tot_custom_duty_additional_charge,
                            "credit": 0.0,
                            "currency_id": self.currency_id.id,
                            "amount_currency": self.tot_custom_duty_additional_charge,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Total Tax Amount",
                            "account_id": self.account_move_id.company_id.import_custom_duty_account_id.id,
                            "debit": self.total_tax_amount,
                            "credit": 0.0,
                            "currency_id": self.currency_id.id,
                            "amount_currency": self.total_tax_amount,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Total Amount Payable",
                            "account_id": self.account_move_id.company_id.import_default_tax_account_id.id,
                            "debit": 0.0,
                            "credit": self.total_amount_payable,
                            "currency_id": self.currency_id.id,
                            "amount_currency": -self.total_amount_payable,
                        },
                    ),
                ],
            }
        )
        move.action_post()
        self.account_move_id.custom_journal_entry_id = move.id

    def button_draft(self):
        if self.account_move_id.custom_journal_entry_id:
            self.account_move_id.is_confirmed_boe = False
            self.account_move_id.custom_journal_entry_id.button_draft()
            self.account_move_id.custom_journal_entry_id = False

    def refund_moves(self):
        reversal_wizard = self.env["account.move.reversal"].create(
            {
                "move_ids": [self.custom_journal_entry_id.id],
                "journal_id": self.journal_id.id,
                "reason": "No reason",
            }
        )
        reversal_wizard.refund_moves()
