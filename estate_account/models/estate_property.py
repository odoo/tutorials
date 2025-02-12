from odoo import Command,models
from odoo.exceptions import AccessError, UserError

class InheritEstateProperty(models.Model):
    _inherit = "estate.property"


    def action_property_sold(self):
        try:
            self.check_access("write")
            self.check_access("write")
        except AccessError:
            raise AccessError(
                "You do not have the necessary permissions to mark this property as sold."
            )
        if not self.partner_id:
            raise UserError("Please define a buyer for the property before marking it as sold.")
        if not self.selling_price:
            raise UserError("Selling price must be set before marking the property as sold.")
        invoice_vals = {
            "partner_id": self.partner_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": "Commission (6% of Selling Price)",
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fee",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }
                ),
            ],
        }
        self.env["account.move"].sudo().create(invoice_vals)
        return  super().action_property_sold()
        
