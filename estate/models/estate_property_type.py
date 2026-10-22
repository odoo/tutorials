from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence", default=1)

    _check_name_unique = models.Constraint(
        'unique(name)',
        'Property type name must be unique.'
    )
