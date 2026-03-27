from odoo import models, fields
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    deal_id = fields.Many2one("estate.property.deal")

    def action_open_deal(self):
        self.ensure_one()

        if not self.deal_id:
            raise ValidationError("Offer is not accepted yet !!")

        self.deal_id.property_id = self.id
        return {
            "type": "ir.actions.act_window",
            "name": "Deal",
            "res_model": "estate.property.deal",
            "view_mode": "form",
            "res_id": self.deal_id.id,
            "target": "current",
        }
