# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for property in self:
            property.check_access("write")
            commission = property.selling_price * 0.06
            discount = property.selling_price * 0.05
            invoice_lines = [
                Command.create(
                    {
                        "name": "6% Commission",
                        "quantity": 1,
                        "price_unit": commission,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }
                ),
                Command.create(
                    {
                        "name": "Discount",
                        "quantity": 1,
                        "price_unit": -discount,
                    }
                ),
            ]
            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines,
            }
            self.env["account.move"].sudo().create(invoice_vals)
        return super().action_sold()
