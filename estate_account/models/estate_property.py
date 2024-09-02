from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_button(self):
        super().action_sold_button()
        move_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                "name": "6% selling price",
                "quantity": 1,
                "price_unit": self.selling_price * 0.6
            }),
                Command.create({
                    "name": "Administration fee",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        }
        self.env['account.move'].check_access_rights('create')
        self.env['account.move'].check_access_rule('create')
        self.env['account.move'].sudo().create(move_vals)

        # self.env['account.move.line'].create({
        #         "move_id": invoice.id,
        #         "name": "6% selling price",
        #         "quantity": 1,
        #         "price_unit": self.selling_price * 0.6
        #     })
