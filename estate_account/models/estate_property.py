from odoo import Command, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def property_action_sell(self):
        for record in self:
            record.check_access('write')
            self.env["account.move"].sudo().create({
                "invoice_origin": self.name,
                "partner_id": self.buyer_id.id, 
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

        return super().property_action_sell()
