from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_ids = fields.One2many("estate.property", "invoice_id", string="Property")

    def action_view_property(self):
        self.ensure_one()
        property_ids = self.property_ids
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "estate.property",
            "res_id": property_ids[0].id,
            "name": _("Property"),
            "views": [[False, "form"]],
            "context": {"create": False},
            "domain": [("id", "in", property_ids.ids)],
        }
        return action_window
