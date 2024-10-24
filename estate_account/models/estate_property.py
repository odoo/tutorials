from odoo import Command, models  
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_button(self):
        invoice_price = {
            "name": self.name,
            "quantity": 1,
            "price_unit": 0.06 * self.selling_price
        }

        administrative_fees = {
            "name": "Administrative Fees",
            "quantity": 1,
            "price_unit": 100
        }

        try:
            self.env['account.move'].check_access_rights('write')
            self.env['account.move'].check_access_rule('write')
        except AccessError:
            raise UserError(("You don't have the access to perform this action!"))

        self.env['account.move'].sudo().create(
            {
                "name": self.name + " Invoice",
                "partner_id" : self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(invoice_price),
                    Command.create(administrative_fees)
                ]
            }
        )
        return super().sold_button()
