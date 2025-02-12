from odoo import Command, fields, models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    def property_action_sell(self):
        print(" reached ".center(100, "="))
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")

            self.env["account.move"].create({
                "partner_id": self.partner_id.id, 
                "move_type": "out_invoice", 
                "invoice_line_ids": [
                    Command.create({
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        }),
                    Command.create({
                        "name": "Commission Fee (6% of Selling Price)",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fee",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),
                ],   
            })

            record.state = "sold" 

        return super().property_action_sell()
