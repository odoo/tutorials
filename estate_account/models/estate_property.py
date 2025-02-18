from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit="estate.property"

    invoice_id = fields.Many2one(comodel_name="account.move")

    def action_mark_property_sold(self):
        res = super().action_mark_property_sold();

        self.check_access('write')
        invoice = self.env["account.move"].sudo().create({
            "partner_id": self.buyer_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": "Property Sale Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00
                }),
            ],
        })

        self.invoice_id = invoice.id
        return res
