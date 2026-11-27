from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_property_sold(self):
        res = super().action_property_sold()
        for prop in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'partner_id': prop.buyer_id.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': prop.name,
                        'quantity': 1,
                        'price_unit': prop.selling_price * (6 / 100)}),
                    (0, 0, {
                        'name': 'administration fees',
                        'quantity': 1,
                        'price_unit': 100
                    })],
        })

        return res
