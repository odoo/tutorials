from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    dashboard_config = fields.Json(
        default=lambda self: self._default_dashboard_config()
    )

    def _default_dashboard_config(self):
        return {"hidden_items": []}

    @api.model
    def get_dashboard_config(self):
        return self.env.user.dashboard_config or {}

    @api.model
    def update_dashboard_config(self, to_hide, to_show):
        config = self.env.user.dashboard_config or {}
        hidden = set(config.get("hidden_items", []))

        hidden.update(to_hide)
        hidden.difference_update(to_show)

        config["hidden_items"] = list(hidden)

        self.env.user.write({"dashboard_config": config})
