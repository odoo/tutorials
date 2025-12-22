from odoo import models


class SignRequestItem(models.Model):
    _inherit = "sign.request.item"

    def _get_user_stamp(self, stamp_type='stamp_sign_stamp'):
        self.ensure_one()
        stamp_user = self.partner_id.user_ids[:1]
        if stamp_user and stamp_type in ['stamp_sign_stamp']:
            return stamp_user[stamp_type]
        return False

    def _get_user_stamp_frame(self, stamp_type='stamp_sign_stamp_frame'):
        self.ensure_one()
        stamp_user = self.partner_id.user_ids[:1]
        if stamp_user and stamp_type in ['stamp_sign_stamp_frame']:
            return stamp_user[stamp_type]
        return False
