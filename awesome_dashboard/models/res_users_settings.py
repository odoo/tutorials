# models/res_users.py
from odoo import models, fields

class ResUsersSettings(models.Model):
    _inherit = ["res.users.settings"]

    disabled_items = fields.Char(
        string="Awesome Dashboard Disabled Items",
    )
