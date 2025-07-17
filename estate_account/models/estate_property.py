from odoo import fields, models, Command


class EstateProperty(models.Model):

    _inherit = "estate.property"

    def action_sold(self):
        res = super().action_sold()
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": fields.Date.today(),
                    # "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": prop.name,
                                "quantity": 1,
                                "price_unit": prop.selling_price,
                            },
                        ),
                        Command.create(
                            {
                                "name": "Administrative fees",
                                "quantity": 1,
                                "price_unit": 100.00,
                            },
                        ),
                    ],
                }
            )
        return res
