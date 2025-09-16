from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'name'
    
    name = fields.Char("Property Type", required=True)
    _unique_name = models.Constraint(
        'unique(name)',
        "Property type name must be unique.",
    )

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Properties",
    )
