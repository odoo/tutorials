from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        res = super().action_send_mail()

        if self.env.context.get("mark_property_as_sold"):
            properties = self.env["estate.property"].browse(
                self.env.context.get("property_ids_to_sell", [])
            )
            properties.action_finalize_sale()

        return res
