from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    dashboard_config = fields.Text("Dashboard Configuration")
    