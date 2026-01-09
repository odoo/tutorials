from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "name"

    sequence = fields.Integer('Sequence', default=1, help="Used to order Property Type")
    name = fields.Char("Property Type", required=True)
    property_ids = fields.One2many('estate.property', "property_type_id", required=True)
    # SQL CONSTRAINT
    _property_type_uniq = models.Constraint(
        'UNIQUE(name)', "Property Type already exist in database"
    )
