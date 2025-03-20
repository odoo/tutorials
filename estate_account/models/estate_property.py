from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        res = super().action_sell_property()

        create_vals = [{
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": property.selling_price,
                    }),
                    Command.create({
                        "name": "Taxes",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ]
            } for property in self]
        self.env["account.move"].create(create_vals)
        
        return res
