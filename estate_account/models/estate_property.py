from markupsafe import Markup

from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        super().action_sold_property()

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

        # Mail wizard
        template_id = self.env.ref("estate.email_template_sold")

        ctx = {
            "default_model": "estate.property",
            # email_from
            "default_res_ids": self.ids,
            # email_to
            "default_partner_ids": self.buyer_id.ids,
            "default_composition_mode": "comment",
            # "default_composition_mode": "mass_mail",
            "default_template_id": template_id.id if template_id else False,
        }

        action = {
            "name": self.env._("Send"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "target": "new",
            "context": ctx,
        }

        return action
