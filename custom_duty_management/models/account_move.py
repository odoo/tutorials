from odoo import fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    show_bill_of_entry = fields.Boolean(default=False, compute="_compute_show_bill_of_entry")
    bill_of_entry_no = fields.Char(string="Bill of Entry No")
    reference = fields.Char(string="reference",readonly=True,)
    custom_currency_rate = fields.Float(string="Custom Currency Rate")
    bill_of_entry_date = fields.Date(string="Bill of Entry Date")
    port_code = fields.Many2one("l10n_in.port.code", string="Port Code")
    journal_move_id = fields.Many2one("account.move", string="Journal Entry", readonly=True)
    bill_of_entry_line_ids = fields.One2many("account.move.bill.of.entry.line", "move_id", string="Bill of Entry Details")\

    # montetary fields
    total_cd_all = fields.Monetary("Total Custom Duty + Additional Charges", currency_field="company_currency_id")
    total_tax_all = fields.Monetary("Total Tax Amount", currency_field="company_currency_id")
    total_amount_all = fields.Monetary("Total Amount Payable", currency_field="company_currency_id")

    # Bill of Entry Button Condition
    def _compute_show_bill_of_entry(self):
        if self.state == "posted" and self.l10n_in_gst_treatment in [
            "overseas",
            "special_economic_zone",
            "deemed_export",
        ]:
            self.show_bill_of_entry = True
        else:
            self.show_bill_of_entry = False

    # Action to open Bill of Entry wizard
    def action_open_bill_of_entry_wizard(self):
        return {
            "name": "Bill of Entry",
            "type": "ir.actions.act_window",
            "res_model": "bill.of.entry.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_move_id": self.id,
                "default_reference": self.name,
            },
        }

    # Action to open Journal Entry through Bill of Entry Stat Button
    def action_open_journal_entry(self):
        """Opens the Journal Entry form view."""
        if not self.journal_move_id:
            raise UserError("No Journal Entry found!")

        return {
            "name": "Journal entry",
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.journal_move_id.id,
            "target": "current",
        }
