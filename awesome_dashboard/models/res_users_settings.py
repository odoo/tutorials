from odoo import fields, models


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    stats_visibility = fields.Text(defualt="")
