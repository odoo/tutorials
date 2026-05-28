from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    awesome_dashboard_config = fields.Char(default='[]')
