from odoo import api, Command, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    @api.model_create_multi
    def action_sold(self):
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids' : [
                    Command.create({'name' : record.name,
                        'quantity' : 1,
                        'price_unit' : record.selling_price * 0.06
                    }),
                    Command.create({'name' : 'Administrative fees',
                        'quantity' : 1,
                        'price_unit': 100.00
                    })
                ]
            }
            self.env['account.move'].create(invoice_vals)
        return super().action_sold()
