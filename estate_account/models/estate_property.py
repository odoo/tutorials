# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, Command
from odoo.exceptions import UserError, AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_property_sold(self):
        res = super().action_property_sold()
        journal = self.env["account.journal"].sudo().search([("type", "=", "sale")], limit=1)
        if not journal:
            raise UserError("No sales journal found!")
        for property in self:
            if not property.buyer_id:
                continue
            try:
                property.check_access('write')
            except AccessError as e:
                raise UserError(f"You don't have permission to modify {property.name}") from e

            self.env["account.move"].sudo().create({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "company_id": property.company_id.id,
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Commission (6%)",
                            "quantity": 1,
                            "price_unit": property.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            })
        return res
