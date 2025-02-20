from odoo import Command, models

class InheritEstateProperty(models.Model):
    _inherit = "estate.property"


    def action_property_sold(self):
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
        