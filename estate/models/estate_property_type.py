from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(
        related="property_ids.offer_ids", store=True, inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")
    _sql_constraints = [("unique_name", "unique(name)", "The name must be unique")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
