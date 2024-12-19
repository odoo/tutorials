from odoo import models, fields, api, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property' 

    def action_sold(self):
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit':record.selling_price
                    }),
                    Command.create({
                        'name': 'Administrative Taxes',
                        'quantity': 1,
                        'price_unit': .06 * record.selling_price if .06 * record.selling_price < 100 else 100
                    })
                ]})
            return super(EstateProperty, self).action_sold()
