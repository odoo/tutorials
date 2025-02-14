from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        for record in self:
            invoice_id = record.env['account.move'].create({
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1.0,
                        "price_unit": record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Admin",
                        "quantity": 1.0,
                        "price_unit": 100,
                    })
                ]
            })
        return super().sell_property()
