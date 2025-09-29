from odoo import models, fields

class UserDashboardSettings(models.Model):
    _name = "user.dashboard.settings"
    _description = "User Dashboard Settings"

    user_id = fields.Many2one('res.users', string="User", required=True)
    disabled_items = fields.Char(string='Dashboard Disabled Items') # Add this Field
