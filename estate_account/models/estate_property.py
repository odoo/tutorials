from odoo import models,Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        try:
            self.check_access("write")
        except:
            raise UserError("You don't have the permission to sold on this record")

        print(" reached ".center(100, '='))
        self.env["account.move"].sudo().create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            'invoice_line_ids': [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 1.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
                ],
        })
        return super().action_sold()
