from odoo import models


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def _get_user_stamp(self):
        self.ensure_one()
        sign_user = self.partner_id.user_ids[:1]
        if sign_user:
            return sign_user['sign_stamp']
        return False

    def _get_user_stamp_frame(self):
        self.ensure_one()
        sign_user = self.partner_id.user_ids[:1]
        if sign_user:
            return sign_user['sign_stamp_frame']
        return False
