from odoo import models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]
    _name = "estate.property"

    def action_set_sold(self):
        for record in self:
            datas_invoice = {
                "partner_id": record.partner_id.id,
                "move_type": 'out_invoice',
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% Commission",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "admnistrative fees",
                        "quantity": 1,
                        "price_unit": 100.00
                    })
                ]
            }
            self.env['account.move'].create(datas_invoice)
        return super().action_set_sold()
