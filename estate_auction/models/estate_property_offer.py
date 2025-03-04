# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    offer_type = fields.Selection(
        [("regular", "Regular"), ("auction", "Auction")], default="regular")

    def action_accept_offer(self):
        self.is_property_for_auction("Accept")
        super().action_accept_offer()
        for record in self:
            template = self.env.ref(
                'estate_auction.mail_template_offer_notification')
            if template:
                template.send_mail(record.id, force_send=True)
            else:
                raise UserError(
                    "Mail Template not found. Please check the template.")

    def action_refuse_offer(self):
        self.is_property_for_auction("Refuse")
        super().action_refuse_offer()
        template = self.env['mail.template'].browse(
            self.env.ref('estate_auction.mail_template_offer_notification').id)
        if template:
            template.send_mail(self.id, force_send=True)
        else:
            raise UserError(
                "Mail Template not found. Please check the template.")

    def is_property_for_auction(self, status):
        if self.property_id.sale_type == 'auction':
            raise UserError(
                f"You Can't {status} Offer Manually due to Auction")
