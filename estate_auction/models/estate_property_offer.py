# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    def get_max_required_price(self, property):
        if property.selling_mode == "auction":
            return property.expected_price
        return super().get_max_required_price(property)

    def action_accept_offer(self):
        if self.property_id.selling_mode == "auction":
            accept_mail_template = self.env.ref("estate_auction.mail_template_offer_accepted")
            reject_mail_template = self.env.ref("estate_auction.mail_template_offer_rejected")
            accept_mail_template.send_mail(self.id, force_send=True)
            refused_offers = self.search([("property_id", "=", self.property_id.id), ("id", "!=", self.id)])
            for offer in refused_offers:
                reject_mail_template.send_mail(offer.id, force_send=True)
        super().action_accept_offer()
