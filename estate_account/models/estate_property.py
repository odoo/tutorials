from odoo import models,Command

class EstateProperty(models.Model):
    _description = "Estate Account property Model"
    _inherit="estate.property"

    def action_mark_property_sold(self):
        self.env["account.move"].create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                    Command.create({
                        "name" : "Property Sale Commission",
                        "quantity" : 1,
                        "price_unit" : 0.06 * self.selling_price,
                   }),
                   Command.create({
                        "name" : "Additional Fees",
                        "quantity" : 1,
                        "price_unit" : 100   
                   })
            ],
        })
        return super().action_mark_property_sold()
