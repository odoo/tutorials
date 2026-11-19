from markupsafe import Markup

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        action = super().action_sold_property()

        invoice = self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of Selling Price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100,
                        },
                    ),
                ],
            }
        )

        # Post message in chatter
        self.message_post(
            body=Markup("Customer invoice created: %s")
            % invoice._get_html_link(title="View Invoice")
        )

        return action

    def action_view_invoices(self):
        return {
            "name": self.env._("Invoices"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [
                ("partner_id", "=", self.buyer_id.id),
                ("move_type", "=", "out_invoice"),
            ],
            "context": {"default_partner_id": self.buyer_id.id},
        }
