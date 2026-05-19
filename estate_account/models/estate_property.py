from odoo import models
from odoo.orm.commands import Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"
    _description = "Inherited Estate Property For Estate Account Module"

    def action_set_sold(self):
        result = super().action_set_sold()
        for estate_property in self:
            self.env['account.move'].create({
                "partner_id": estate_property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% selling price",
                        "quantity": 1,
                        "price_unit": estate_property.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "admin fees",
                        "quantity": 1,
                        "price_unit": 100000
                    })
                ]
            })
        return result
