from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        for estate_property in self:
            new_invoice = {"partner_id": estate_property.buyer.id, "move_type": "out_invoice",
                           "line_ids": [
                               Command.create({
                                   "name": "6% of selling price",
                                   "quantity": 1,
                                   "price_unit": estate_property.selling_price * 0.06
                               }),
                               Command.create({
                                   "name": "Administrative fees",
                                   "quantity": 1,
                                   "price_unit": 100
                               })
                           ]
                           }
            self.env["account.move"].create(new_invoice)

        return super().action_property_sold()
