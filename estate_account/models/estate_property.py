from odoo import api, models, fields, exceptions, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        if not self.buyer_id:
            raise exceptions.UserError("A buyer must be set before selling the property.")

        self.check_access('write')

        invoicing_price = self.selling_price * 0.06
        admin_fee = 100

        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": invoicing_price,
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": admin_fee,
                }),
            ],
        }
        self.env['account.move'].sudo().create(invoice_vals)

        return super(EstateProperty, self).action_sell_property()
