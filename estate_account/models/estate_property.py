from odoo import models, Command, exceptions


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def property_sold(self):

        for prop in self:
            prop.check_access('write')

        self.sudo().env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.buyer_id .id,
            "name": f"INV/2025/{self.id}",
            "line_ids": [
                Command.create({"name": self.name, "quantity": 1, "price_unit": 0.06 * self.selling_price}),
                Command.create({"name": "Administrative Fees", "quantity": 1, "price_unit": 100.0})
            ]
        })
        return super().property_sold()
