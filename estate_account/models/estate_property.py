from odoo import Command, fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_change_state(self):
        param_value = self.env.context.get("param_name", "default_value")
        if param_value == "sold":
            for record in self:
                record.state = "sold"
                values = {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "state": "draft",
                    "invoice_date": fields.Date.today(),
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": record.display_name,
                                "price_unit": record.selling_price,
                                "quantity": 1,
                            }
                        ),
                        Command.create(
                            {
                                "name": '"6%" of Property Sale Price',
                                "quantity": 1,
                                "price_unit": record.selling_price * 0.06,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Fees",
                                "quantity": 1,
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
                self.env["account.move"].sudo().create(values)
        else:
            return super().action_change_state()
