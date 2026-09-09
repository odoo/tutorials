from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer()

    property_id = fields.One2many(
        "estate.property",
        "property_type_id",
    )
    offer_id = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(
        compute="_count_offer_ids",
    )

    _check_property_type_name = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique",
    )

    @api.depends("offer_id")
    def _count_offer_ids(self):
        for record in self:
            record.offer_count = len(record.offer_id)
