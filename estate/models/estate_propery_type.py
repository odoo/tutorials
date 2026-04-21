from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name asc"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    expected_price = fields.Float()
    state = fields.Char()
    offer_count = fields.Char(compute="_compute_offer")

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_offer(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Propery Offers",
            "res_model": "estate.property.offer",
            "domain": [("property_id", "=", self.id)],
            "view_mode": "list,form",
            "context": {"default_property_id": self.id},
        }
