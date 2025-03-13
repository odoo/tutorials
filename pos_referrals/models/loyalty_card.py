# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, fields, models


class LoyaltyCardReferral(models.Model):
    _inherit = "loyalty.card"

    referrer_id = fields.Many2one("res.partner", string="Referral From", readonly=True)

    @api.model
    def create_referral_gift_card(self, partner_id, order_amount):
        referral_program = self.env["loyalty.program"].search([("name", "=", "Gift Cards")], limit=1)
        if not referral_program:
            return False
        customer = self.env["res.partner"].browse(partner_id)
        if not customer or not customer.referred_by:
            return False
        expiry_date = fields.Date.today() + timedelta(days=90)
        reward_amount = order_amount * 0.10
        gift_card = self.create({
            "partner_id": customer.referred_by.id,
            "expiration_date": expiry_date,
            "points": reward_amount,
            "program_id": referral_program.id,
            "referrer_id": customer.id,
            "active": True,
        })
        return True
