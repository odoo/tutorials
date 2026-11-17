from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        res = super().action_send_mail()
        if (
            self.env.context.get("mark_property_sold")
            and self.model == "estate.property"
        ):
            props = self.env["estate.property"].browse(self._evaluate_res_ids())
            props._create_invoice()
        return res
