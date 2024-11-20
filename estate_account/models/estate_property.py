from odoo import models, Command, api, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_ids = fields.One2many("account.move", "property_id", string="Invoices")

    invoice_count = fields.Integer(compute="_calc_invoices", string="Invoice Count")

    @api.depends("invoice_ids")
    def _calc_invoices(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def onclick_sold(self):
        super().onclick_sold()
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "property_id": self.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Property selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "6% of the selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative price",
                            "quantity": 1,
                            "price_unit": 100,
                        }
                    ),
                ],
            }
        )
        return True
