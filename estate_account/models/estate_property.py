from odoo import fields, models
from odoo.fields import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    property_ids = fields.One2many(
        "estate.property", inverse_name="salesman_id", string="Properties"
    )

    def action_state(self):
        action = self.env.context.get("action")
        for record in self:
            if action == "sell":
                journal = record.env["account.journal"].search(
                    [("type", "=", "sale"), ("company_id", "=", record.env.company.id)]
                )
                self.env["account.move"].create(
                    [
                        {
                            "move_type": "out_invoice",
                            "partner_id": record.buyer_id.id,
                            "journal_id": journal.id,
                            "invoice_line_ids": [
                                Command.create(
                                    {
                                        "name": record.name,
                                        "quantity": 1,
                                        "price_unit": record.selling_price * 0.06,
                                    }
                                ),
                                Command.create(
                                    {
                                        "name": "Admin. fees",
                                        "quantity": 1,
                                        "price_unit": 100,
                                    }
                                ),
                            ],
                        }
                    ]
                )
        return super().action_state()
