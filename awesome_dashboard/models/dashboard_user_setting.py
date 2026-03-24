from odoo import fields, models


class UserSetting(models.Model):
    _name = "dashboard.user.setting"
    _description = "User Settings"

    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")
    removed_ids = fields.Json("Removed Cards")
