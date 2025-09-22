from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def set_state_sold(self):
        for record in self:
            values = {}
            values["partner_id"] = record.buyer_partner_id.id
            values["move_type"] = "out_invoice"
            values["invoice_line_ids"] = [
                Command.create(
                    {
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * (6 / 100),
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }
                ),
            ]

            self.env["account.move"].create(values)
        return super().set_state_sold()
