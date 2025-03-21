from datetime import timedelta
from odoo import api, fields, models


class LoyaltyCardReferral(models.Model):
    _inherit = "loyalty.card"

    referrer_id = fields.Many2one("res.partner", string="Referral From", readonly=True)

    @api.model
    def create_referral_gift_card(self, partner_id, order_amount, pos_order_id):
        if not partner_id or not order_amount:
            return False

        customer = self.env["res.partner"].browse(partner_id)
        if not customer.exists() or not customer.referred_by:
            return False

        referral_program = self.env["loyalty.program"].sudo().search([
            ("name", "=", "Referral Gift Cards")
        ], limit=1)
        if not referral_program:
            return False

        gift_card_points = round(order_amount * 0.10, 2)
        gift_card = self.create({
            "partner_id": customer.referred_by.id,
            "referrer_id": customer.id,
            "program_id": referral_program.id,
            "expiration_date": fields.Date.today() + timedelta(days=90),
            "points": gift_card_points,
            "active": True,
        })

        self.env["loyalty.history"].create({
            "card_id": gift_card.id,
            "description": f"Referral gift card earned by {customer.name}'s order",
            "issued": gift_card_points,
            "order_model": "pos.order",
            "order_id": pos_order_id,
        })

        second_referrer = customer.referred_by.referred_by
        if second_referrer:
            loyalty_program = self.env["loyalty.program"].sudo().search([
                ("program_type", "=", "loyalty")
            ], limit=1)
            if loyalty_program:
                loyalty_card = self.search([
                    ("program_id", "=", loyalty_program.id),
                    ("partner_id", "=", second_referrer.id)
                ], limit=1)
                if not loyalty_card:
                    loyalty_card = self.create({
                        "partner_id": second_referrer.id,
                        "program_id": loyalty_program.id,
                        "points": 0,
                        "active": True,
                    })
                extra_points = round(order_amount / 2, 2)
                loyalty_card.points += extra_points
                self.env["loyalty.history"].create({
                    "card_id": loyalty_card.id,
                    "description": f"Loyalty points earned from referral chain (order by {customer.name})",
                    "issued": extra_points,
                    "order_model": "pos.order",
                    "order_id": pos_order_id,
                })

        return True
