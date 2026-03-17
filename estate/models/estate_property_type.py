from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'


    name = fields.Char(required = True)



    _check_unique_tag = models.Constraint(
        'UNIQUE(name)', "A property type name must be unique!"
    )
