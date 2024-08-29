import logging
from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        logging.info("Request to create the invoices of property")
        self.check_access_rights("write")
        self.check_access_rule("write")
        for record in self:
            values_property = {
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "line_ids": [
                    Command.create(
                        {
                            "name": record.name,
                            "quantity": 1,
                            "price_unit": 0.06 * record.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "administrative_fees",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        self.env["account.move"].sudo().create(values_property)
        return super().action_set_sold()
