from odoo import fields, models

SIGN_USER_FIELDS = ['sign_stamp']


class ResUsers(models.Model):
    _inherit = 'res.users'

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + SIGN_USER_FIELDS

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + SIGN_USER_FIELDS

    sign_stamp = fields.Binary(string="Digital Stamp", copy=False, groups="base.group_user")
    sign_stamp_frame = fields.Binary(string="Digital Stamp Frame", copy=False, groups="base.group_user")
