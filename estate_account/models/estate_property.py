from odoo import models, Command


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def action_set_sold(self):
        journal_sales = self.env['account.journal'].search([('name', '=', 'Sales')])
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal_sales.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price*6/100,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
            ]
        })
        return super().action_set_sold()