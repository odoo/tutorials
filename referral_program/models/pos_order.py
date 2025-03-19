# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def generate_gift_card(self, coupon_data):
        if coupon_data:
            giftcard_program = self.env.ref('loyalty.gift_card_program', raise_if_not_found=False)
            if giftcard_program:
                coupon_data['program_id'] = giftcard_program.id
                coupon_data['code'] = self.env['loyalty.card']._generate_code()
                self.env['loyalty.card'].with_context(action_no_send_mail=True).create(coupon_data)
