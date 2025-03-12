from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    show_bill_of_entry = fields.Boolean(default=False, compute="_compute_show_bill_of_entry")

    def _compute_show_bill_of_entry(self):
        if(self.state == "posted" and self.l10n_in_gst_treatment in ["overseas","special_economic_zone", "deemed_export"]):
            self.show_bill_of_entry = True
        else:
            self.show_bill_of_entry = False

    def action_open_bill_of_entry_wizard(self):
        return {
            "name" : "Bill of Entry",
            "type" : "ir.actions.act_window",
            "res_model" : "bill.of.entry.wizard",
            "view_mode" : "form",
            "target" : "new",
            "context" : {"default_move_id":self.id},
        }
