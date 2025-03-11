from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_ids = fields.One2many(string="Invoice", comodel_name="account.move", inverse_name="estate_property_id")

    def action_sold_button(self):
        self.check_access('write')
        moves = self.env['account.move'].sudo().create({
            'partner_id' : self.buyer_id.id,
            'move_type' : 'out_invoice',
            'estate_property_id' : self.id,
            'invoice_line_ids' : [
                Command.create({
                    'name' : self.name,
                    'quantity' :  1,
                    'price_unit' : self.selling_price * 0.06
                }),
                Command.create({
                    'name' : 'Administrative fees',
                    'quantity' :  1,
                    'price_unit' : 100
                })
            ]
        })
        return super().action_sold_button()
