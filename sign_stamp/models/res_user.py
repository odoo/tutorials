from odoo import models, fields

SIGN_USER = ["sign_stamp"]


class ResUsers(models.Model):
    _inherit = "res.users"

    @property
    def readable_field(self):
        return super().readable_field + SIGN_USER

    @property
    def writeable_field(self):
        return super().writeable_field + SIGN_USER

    stamp_sign_stamp = fields.Binary(
        string="Company Stamp", copy=False, groups="base.group_user"
    )
    stamp_sign_stamp_frame = fields.Binary(
        string="Company Stamp Frame", copy=False, groups="base.group_user"
    )
