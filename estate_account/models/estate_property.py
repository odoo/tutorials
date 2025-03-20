from odoo import api, fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_sold(self):
        invoice_lines = [{
            'partner_id': property.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                fields.Command.create({
                    'name': '6% of selling price',
                    'quantity': 0.06,
                    'price_unit': property.selling_price,
                }),
                fields.Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 10000,
                }),
            ]} for property in self]
        self.env['account.move'].create(invoice_lines)
        return super().action_mark_sold()
