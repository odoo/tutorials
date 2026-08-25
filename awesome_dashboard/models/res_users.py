from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    dashboard_disabled_items = fields.Char(default='[]')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['dashboard_disabled_items']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['dashboard_disabled_items']
