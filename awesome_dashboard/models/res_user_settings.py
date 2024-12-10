from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    dashboard_config = fields.Json(string="Dashboard Configuration", readonly=True)
