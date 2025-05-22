from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"
    _order = "sequence, name"

    name = fields.Char(required=True)

    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many("estate.property", "type_id", string="Properties")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique')
    ]

    def _compute_offer_count(self):
        for propertyType in self:
            propertyType.offer_count = len(propertyType.offer_ids)
