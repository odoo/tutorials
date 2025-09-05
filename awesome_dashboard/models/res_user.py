from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    disabled_dashboard_items = fields.Text(
        string="Disabled Dashboard Items",
        help="Stores list of dashboard item IDs hidden by this user",
    )

    @api.model
    def save_disabled_dashboard_items(self, disabled_items_json):
        self.env.user.disabled_dashboard_items = disabled_items_json
        return True

    @api.model
    def get_disabled_dashboard_items(self):
        return self.env.user.disabled_dashboard_items or "[]"
