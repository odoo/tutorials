from odoo import fields, models # type: ignore

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'This property type name already exists'),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id", string="Property")

