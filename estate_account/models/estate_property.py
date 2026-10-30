from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_as_sold(self):
        if not self.env['account.journal'].search([('type', '=', 'sale'), ('code', '=', 'TUTO')]):
            self.env['account.journal'].create({
                'type': 'sale',
                'company_id': self.env.company.id,
                'name': 'Tutorial Journal',
                'code': 'TUTO',
            })

        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('name', '=', 'Tutorial Journal')]).id,
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': "Tax",
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100.00,
                })
            ]
        })
        return super().action_mark_as_sold()
