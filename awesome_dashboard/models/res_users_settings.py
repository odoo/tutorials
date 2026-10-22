from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    awesome_dashboard_disabled_items = fields.Char(
        string="Disabled dashboard items",
        default="",
    )
