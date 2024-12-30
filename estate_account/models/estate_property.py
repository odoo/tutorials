from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"
    _description = "Estate Property"

    def action_property_sold(self):
        for record in self:
            record.check_access('create')

            if not record.buyer_id:
                raise UserError("The property must have a buyer before marking it as sold.")

            # create empty 'account.move' object for sold property
            account_move_values = {
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "warranty_line_ids": [
                    # First invoice line: 6% of the selling price
                    Command.create(
                        {
                            "name": f"Property {record.name} Selling Price",
                            "quantity": 1,
                            "price_unit": record.selling_price * 0.06,
                        }
                    ),
                    # Second invoice line: Administrative fee of 100
                    Command.create(
                        {
                            "name": "Administrative Fee",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
            record.env["account.move"].create(account_move_values)
        return super().action_property_sold()
