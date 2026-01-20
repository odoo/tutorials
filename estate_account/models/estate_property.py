from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"   # extend existing estate.property model

    # Override the action_sold method
    def action_sold(self):
        res = super().action_sold()  # Call the original method

        for property_record in self:
            if property_record.partner_id:  # check if the property has a buyer
                invoice_vals = {
                    "partner_id": property_record.partner_id.id,
                    "move_type": "out_invoice",  # customer invoice
                    "invoice_line_ids": [
                        Command.create({
                            "name": f"Commission for property: {property_record.name}",
                            "quantity": 1,
                            "price_unit": property_record.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }),
                    ],
                }
                self.env["account.move"].create(invoice_vals)  # Create the invoice
        return res
