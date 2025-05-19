from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    _sql_constraints = [
        ("positive_bill_of_entry_custom_currency_rate", "CHECK(bill_of_entry_custom_currency_rate > 0)", "Custom currency rate for bill of entry must be strictly positive.")
    ]
        
    bill_of_entry_id = fields.Many2one(comodel_name="account.move", string="Bill of Entry", copy=False)
    bill_of_entry_custom_currency_rate = fields.Monetary(string="Custom Currency Rate", currency_field="currency_id", copy=False)
    l10n_in_custom_duty_enabled = fields.Boolean(related="company_id.l10n_in_custom_duty_enabled")

    def action_open_invoice(self):
        self.ensure_one()
        
        if not self.bill_of_entry_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.bill_of_entry_id.id,
            "view_mode": "form",
            "target": "current"
        }
