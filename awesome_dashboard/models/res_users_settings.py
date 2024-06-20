from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    awesome_dashboard_settings = fields.Char()
