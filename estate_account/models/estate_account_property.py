from odoo import models, fields, Command


class EstateAccountProperty(models.Model):
    _inherit = "estate.property"

    invoice_ids = fields.One2many("account.move", "property_id", string="Invoice", copy=False)
    display_invoice_btn = fields.Boolean(default=False)

    def property_set_sold(self):
        for record in self:
            invoice = record.env['account.move'].create({
                "name": record.name,
                "property_id": record.id,
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create({
                        "name": "Deposit (6%)",
                        "quantity": 1,
                        "price_unit": record.selling_price*0.06
                    }),
                    Command.create({
                        "name": "Admin fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ],
            })
            print("New invoice created with id: ", invoice.id)
            record.display_invoice_btn = True
        return super().property_set_sold()
