from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_estate_property_sold(self):
        self.check_access('write')
        print("Sold button clicked from account application")
        super().action_estate_property_sold()
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_date": fields.Date.today(),
                "line_ids": [
                    Command.create(
                        {"name": self.name, "price_unit": self.selling_price}
                    ),
                    Command.create(
                        {"name": "6% tax", "price_unit": self.selling_price * 0.06}
                    ),
                    Command.create({"name": "Administrative Fees", "price_unit": 100}),
                ],
            }
        )
