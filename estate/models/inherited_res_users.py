from odoo import fields, models, api


class InheritedResUsersModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        string="Estate Properties",
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]",
    )
    property_count = fields.Integer(compute="_compute_property_count", string="Offers")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for user in self:
            user.property_count = len(user.property_ids)

    def action_user_property(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Properties",
            "res_model": "estate.property",
            "view_mode": "list,form",
            "domain": [("salesman_id", "=", self.id)],
        }
