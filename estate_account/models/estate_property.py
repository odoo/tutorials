import re

from odoo import models, Command


class EstateAccountPropertyModel(models.Model):
    _inherit = "estate.property"

    def mark_as_sold(self):
        self.ensure_one()
        self.env["account.move"].create({
            "name": self._generate_invoice_name(),
            "partner_id": self.salesperson_id.id,
            "move_type": "out_invoice",
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price
                }),
                Command.create({
                    "name": "VAT",
                    "quantity": 1,
                    "price_unit": self.selling_price * .06
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                })
            ]
        })
        return super().mark_as_sold()

    def _generate_invoice_name(self):
        invoice = self.env["account.move"].search([("name", "like", "Invoice %")], order="id desc", limit=1)
        if invoice and (match := re.match(r"Invoice\s+(\d+)", invoice.name)):
            return f"Invoice {int(match.group(1)) + 1}"
        return "Invoice 1"
