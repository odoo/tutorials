from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"
    contract_ids = fields.One2many("estate.contract", "property_id")

    def action_open_contract(self):
        for record in self:
            return {
                "type": "ir.actions.act_window",
                "res_model": "estate.contract",
                "view_mode": "form",
                "target": "current",
                "context": {
                    "default_property_id": record.id,
                    "default_buyer_id": record.buyer_id.id,
                    "default_price": record.selling_price,
                    "default_salesperson_id": record.user_id,
                },
            }
