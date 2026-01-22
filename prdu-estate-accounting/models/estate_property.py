from odoo import models, fields, Command, exceptions

class estatePropertyInherit(models.Model):
    _inherit = "estate.property"
    
    def action_property_sell(self):
        for record in self:
            if record.selling_price == 0 or record.customer_id is None:
                raise exceptions.UserError("Can't sell a property without a valid accepted offer.")
            movedict = dict()
            movedict["partner_id"] = record.customer_id.id
            movedict["move_type"] = "out_invoice"
            movedict["line_ids"] = [
                Command.create({
                    "name" : record.name,
                    "quantity" : 0.06,
                    "price_unit" : record.selling_price,
                }),
                Command.create({
                    "name" : "A12e f2s",
                    "quantity" : 1,
                    "price_unit" : 100,
                })
            ]
            move = self.env["account.move"].create(movedict)
        return super().action_property_sell()
