from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Type must be unique"),
    ]
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
