from odoo import models, fields


class ResUsersSettings(models.Model):
    _inherit = ["res.users.settings"]

    disabled_dashboard_items = fields.Text("Disabled dashboard items")
