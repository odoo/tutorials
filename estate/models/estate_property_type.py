from odoo import api, fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "This is table contain the types of property"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_uniq = models.Constraint(
        "unique(name)",
        "Property Types must be Unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
