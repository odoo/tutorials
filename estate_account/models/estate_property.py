from odoo import Command, models

class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        for property in self:
            self.env["account.move"].create({
                "partner_id": property.partner_id.id,
                "move_type":"out_invoice",
                "property_id": property.id,
                "line_ids":[
                    Command.create({
                        "name": property.name,
                        "quantity":1,
                        "price_unit": (property.selling_price)*0.06,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity":1,
                        "price_unit": 100.00,
                    })
                ]                
            })
        return super().sold_property()