from odoo import fields, models
from odoo import Command
from odoo.tools.translate import _


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one('account.move', string='Invoice')

    def action_property_sold(self):
        recs = super().action_property_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for record in self:
            inv = self.env['account.move'].create(
                {
                    "partner_id": record.partner_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({"name": record.name,
                                        "quantity": 1.0,
                                        "price_unit": record.selling_price * 0.06}
                                       ),
                        Command.create({"name": "Administration Fees",
                                        "quantity": 1.0,
                                        "price_unit": 100}
                                       ),
                    ]
                }
            )
            record.invoice_id = inv
        return recs

    def action_view_invoice_from_property(self):
        self.ensure_one()
        inv_id = self.invoice_id
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": inv_id.id,
            "name": _("Invoice"),
            "view_mode": "form",
        }
        return action_window
