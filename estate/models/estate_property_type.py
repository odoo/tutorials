from odoo import fields, models, api


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_count_offers")

    @api.depends("offer_ids")
    def _count_offers(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
            print(type.offer_count)

    def action_open_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }
