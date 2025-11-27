from odoo import models, fields

SIGN_USER_FIELDS = ["stamp_sign"]


class ResUsers(models.Model):
    _inherit = "res.users"

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + SIGN_USER_FIELDS

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + SIGN_USER_FIELDS

    stamp_sign_stamp = fields.Binary(
        string="Company Stamp", copy=False, groups="base.group_user"
    )
    stamp_sign_stamp_frame = fields.Binary(
        string="Company Stamp Frame", copy=False, groups="base.group_user"
    )
