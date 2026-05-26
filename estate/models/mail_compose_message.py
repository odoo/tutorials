from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        mail = super().action_send_mail()
        if self.env.context.get('mark_property_sold'):
            properties = self.env['estate.property'].browse(
                self.env.context.get('default_res_ids', []))
            properties._mark_as_sold()

        return mail
