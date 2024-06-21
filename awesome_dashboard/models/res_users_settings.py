from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    awesome_dashboard_items = fields.Char(default="")
