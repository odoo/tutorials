from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property.offer"

    sale_type = fields.Selection(related="property_id.sale_type", store=False)

    def action_accept_offer(self):
        res = super().action_accept_offer()
        for record in self:
            rejected_offers = (
                self.env["estate.property.offer"].search(
                    [("property_id", "=", record.property_id)]
                )
                - record
            )
            template_reject = record.env.ref(
                "estate_auction.mail_template_offer_rejected"
            )
            for offer in rejected_offers:
                template_reject.send_mail(
                    offer.id,
                    email_layout_xmlid="mail.mail_notification_light",
                    email_values={
                        "auto_delete": True,
                        "email_to": offer.partner_id.email_formatted,
                        "email_from": self.env.company.email_formatted,
                    },
                    force_send=True,
                )
        return res
