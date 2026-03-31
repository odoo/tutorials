from odoo import models, fields
import json


class ResUsers(models.Model):
    _inherit = "res.users"

    dashboard_hidden_items = fields.Text()

    def get_dashboard_settings(self):
        self.ensure_one()
        return self.dashboard_hidden_items or "[]"

    def set_dashboard_settings(self, hidden_items):
        self.ensure_one()
        self.sudo().dashboard_hidden_items = json.dumps(hidden_items)
        return True
