from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = "name"

    name = fields.Char("Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _check_type_name = models.Constraint("UNIQUE(name)", "Property type name must be unique")
