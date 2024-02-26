from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    disabled_items = fields.Char(default="[]")
     