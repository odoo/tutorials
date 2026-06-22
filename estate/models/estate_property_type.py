from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    _name_uniq = models.Constraint(
        "unique(name)",
        "A type with the same name already exists.",
    )

    name = fields.Char("Title", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order property-types. Lower is better."
    )

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_offer_count")

    def _offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
