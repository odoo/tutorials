from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_on_sold(self):
        res = super().action_on_sold()

        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": 0.06 * self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
            self.env['account.move'].create(invoice_vals)

        return res
