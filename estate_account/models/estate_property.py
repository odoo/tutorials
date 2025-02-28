from odoo import models, fields, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.check_access('write')
        for record in self:
            invoice = record.env['account.move'].sudo().create({
                'partner_id': record.buyer_id.id,
                'move_type':'out_invoice',
                'name' : f'INV/2025/0000{self.id}',
                'invoice_line_ids':[
                    Command.create({
                        "name":"Charges",
                        "quantity":1,
                        "price_unit":1.06*record.selling_price,
                    }),
                    Command.create({
                        "name":"Additional Charges",
                        "quantity":1,
                        "price_unit":100
                    })
                ]
            })
        return super().action_sold()
