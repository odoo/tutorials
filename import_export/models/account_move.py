from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    is_confirmed_boe = fields.Boolean(
        help="Determines whether journal entry is posted or not."
    )
    custom_journal_entry_id = fields.Many2one(comodel_name="account.move")
    import_export_duty = fields.Boolean(related="company_id.import_export_duty")

    def open_bill_of_entry(self):
        existing = self.env["bill.of.entry"].search([("account_move_id", "=", self.id)], limit=1)
        print(existing.id)
        if existing:
            return {
                "type": "ir.actions.act_window",
                "res_model": "bill.of.entry",
                "view_mode": "form",
                "res_id": existing.id,
                "target": "new",
            }
        return {
            "name": "Bill of Entry Action",
            "type": "ir.actions.act_window",
            "res_model": "bill.of.entry",
            "view_mode": "form",
            "target": "new",
            "context": {"default_move_id": self.id},
        }