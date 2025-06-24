from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    dashboard_disabled_items = fields.Char(default="")

    @api.model
    def set_dashboard_settings(self, disable_item_ids):
        if self.env.user:
            items = ",".join(map(str, disable_item_ids))
            self.env.user.sudo().write({"dashboard_disabled_items": items})
            return True
        return False

    @api.model
    def get_dashboard_settings(self):
        if self.env.user and self.env.user.dashboard_disabled_items:
            return self.env.user.dashboard_disabled_items.split(",")
        return []
