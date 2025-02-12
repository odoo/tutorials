from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        for record in self:
            invoice = record.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type':'out_invoice',
                'invoice_line_ids':[
                    Command.create({
                        "name":"Charges",
                        "quantity":1,
                        "price_unit":1.06*self.selling_price,
                    }),
                    Command.create({
                        "name":"Additional Charges",
                        "quantity":1,
                        "price_unit":100
                    })
                ]
            })
        return super().sold_property()