from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id  = fields.Many2one('account.move', string="Invoice", readonly=True)

    def sell_property(self):
        for record in self:
            if not record.buyer.id:
                raise ValueError("Cannot generate invoice because no buyer is assigned")

            invoice = record.env['account.move'].create({
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
            record.invoice_id = invoice.id

        return super().sell_property()
