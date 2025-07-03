from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    property_sell_type = fields.Selection(related="property_id.property_sell_type")

    def action_accept_offer(self):
        accepted_offer = self
        super().action_accept_offer()

        template_accepted = self.env.ref(
            "automated_estate_auction.mail_template_accept_offer"
        )

        template_accepted.send_mail(accepted_offer.id, force_send=True)

        template_rejected = self.env.ref(
            "automated_estate_auction.mail_template_reject_offer"
        )

        other_offers = self.env["estate.property.offer"].search(
            [
                ("property_id", "=", accepted_offer.property_id.id),
                ("id", "!=", accepted_offer.id),
            ]
        )
        for offer in other_offers:
            template_rejected.send_mail(offer.id, force_send=True)

        return True
