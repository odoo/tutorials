from odoo import Command, models
from odoo.exceptions import UserError


class Property(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise UserError(self.env._("No sale journal found. Please configure an accounting sale journal."))
        for record in self:
            if not record.partner_id:
                raise UserError(self.env._(f"Cannot sell property '{record.name}' because no buyer/partner is assigned."))
            self.env["account.move"].create(
                {
                    "partner_id": record.partner_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            },
                        ),
                        Command.create(
                            {
                                "name": "administrative fees",
                                "price_unit": 100.00,
                            },
                        ),
                    ],
                },
            )
        return super().action_sell_property()
