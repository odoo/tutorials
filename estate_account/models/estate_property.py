from odoo import Command, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property"]

    def action_sold(self):
        res = super().action_sold()
        for record in self:
            vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": "Commission for " + record.name,
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
            self.env["account.move"].create(vals)
        return res
