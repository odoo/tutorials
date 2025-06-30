from odoo import models, Command
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        _logger.warning("🔥 estate_account: action_sold override triggered")

        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            raise UserError("No sale journal found.")

        for prop in self:
            if not prop.buyer_id:
                raise UserError(f"Property '{prop.name}' has no buyer.")

            invoice = self.env["account.move"].create({
                "partner_id": prop.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": prop.name,
                        "quantity": 1.0,
                        "price_unit": prop.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    }),
                ],
            })

            _logger.warning(f"✅ Invoice created for property '{prop.name}' → {invoice.name}")

        return super().action_sold()
