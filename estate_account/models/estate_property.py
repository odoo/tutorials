from odoo import models, fields
from odoo import Command
from odoo.exceptions import UserError


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.properties'

    def action_property_sold(self):
        print(self,'self')
        super().action_property_sold()
        journal = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)
        print(journal,'')

        if not journal:
            raise UserError(
                'No Sales Journal found. Please configure a Sales Journal.')

        for record in self:
            values = {
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'price_unit': record.selling_price,
                        'quantity': 1,
                    }), Command.create({
                        'name': '"6%" of Property Sale Price',
                        'price_unit': record.selling_price*0.06,
                        'quantity': 1,
                    }), Command.create({
                        'name': 'Administrative Fees',
                        'price_unit': 100,
                        'quantity': 1,
                    })

                ]
            }
            self.env['account.move'].sudo().create(values)
