from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = 'res.users.settings'

    dashboard_layout = fields.Char(string="Dashboard Layout", help="Json string to remember dashboard cards visibility")
