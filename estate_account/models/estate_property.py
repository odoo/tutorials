from odoo import Command, fields, models


class InheritedModel(models.Model):
    _inherit = "estate.property"

    state = fields.Selection(
        selection_add=[("invoiced", "Invoiced")], ondelete={"invoiced": "cascade"}
    )

    def action_to_invoice_property(self):
        print("Added successfully".center(100, "="))
        self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Commission",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],
            }
        )
        result = super().action_to_invoice_property()
        self.state = "invoiced"
        return result
