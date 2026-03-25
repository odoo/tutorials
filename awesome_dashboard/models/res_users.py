from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    dashboard_settings = fields.Json(string="Dashboard Settings")
