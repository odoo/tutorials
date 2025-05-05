from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("estate_account: Overridden action_sold triggered")  # For testing
        result = super().action_sold()
        self._create_invoice()

        return result

    def _create_invoice(self):
        for property in self:
            # check if it has a buyer
            if not property.buyer_id:
                continue

            commission = property.selling_price * 0.06
            admin_fee = 100.0

            invoice_vals_list = {
                "name": "Selling " + property.name,
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_origin": property.name,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Commission (6%)",
                            "quantity": 1,
                            "price_unit": commission,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": admin_fee,
                        }
                    ),
                ],
            }

            self.env["account.move"].create(invoice_vals_list)
