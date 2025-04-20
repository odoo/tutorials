from odoo import Command, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        for record in self:
            invoice_vals = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                'invoice_line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            }

            try:
                self.env["estate.property"].check_access("write")
            except AccessError:
                raise AccessError("You don't have the permission to sold on this record")

            self.env['account.move'].sudo().create(invoice_vals)
        return super().action_set_sold()
