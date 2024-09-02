from odoo import fields, models, Command


class EstateProperty(models.Model):

    _inherit = "estate.property"

    def action_sold(self):
        self.check_access_rights('write')
        self.check_access_rule('write')
        move_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            "invoice_line_ids": [
                Command.create({
                    "name": "6% of the selling price",
                    "quantity": 1,
                    "price_unit": 0.6 * self.selling_price
                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": 1,
                    "price_unit": 100.0
                })
            ],

        }
        self.env['account.move'].sudo().create(move_vals)
        return super().action_sold()
