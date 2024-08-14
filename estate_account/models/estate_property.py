from odoo import models, Command
import logging
from datetime import date


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def status_action_sold_button(self):
        logging.info("Request to create the invoices of property")
        for record in self:
            if record.buyer_id:
                partner_id = record.buyer_id.id
                self.env["account.move"].create(
                    {
                        "partner_id": partner_id,
                        "move_type": "out_invoice",
                        "invoice_date": date.today(),
                        "narration": "Tutorials traning",
                        "amount_total": record.selling_price,
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": record.name,
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                    "invoice_date": date.today(),
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Administrative Fee",
                                    "quantity": 1,
                                    "price_unit": 100,
                                    "invoice_date": date.today(),
                                },
                            ),
                        ],
                    }
                )
        return super().status_action_sold_button()
