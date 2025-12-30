from odoo import models


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def _get_user_stamp(self, signature_type='stamp_sign_stamp'):
        self.ensure_one()
        sign_user = self.partner_id.user_ids[:1]
        if sign_user and signature_type in ['stamp_sign_stamp']:
            return sign_user[signature_type]
        return False

    def _get_user_stamp_frame(self, signature_type='stamp_sign_stamp_frame'):
        self.ensure_one()
        sign_user = self.partner_id.user_ids[:1]
        if sign_user and signature_type in ['stamp_sign_stamp_frame']:
            return sign_user[signature_type]
        return False
