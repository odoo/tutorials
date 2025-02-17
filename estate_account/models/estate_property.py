from odoo import exceptions, Command, models
from odoo.exceptions import UserError


class InheritedEstateProperty(models.Model):
    _inherit="estate.property"

    def action_set_sold(self):

        # print(" reached ".center(100, '='))
        self.check_access('write')

        invoice_vals = {
            "name": "Invoice Bill",
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "line_ids": [
                Command.create({
                    "name": "6% of the selling price",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                })
            ]
            }

        print(f"Invoice creation attempt for Buyer ID: {self.buyer_id.id}, Selling Price: {self.selling_price}")


        if not self.env.user.has_group('estate.estate_group_user'):
            raise UserError("You do not have permission to confirm the sale.")
        

        invoice = self.env["account.move"].sudo().create(invoice_vals)

        return super().action_set_sold()
