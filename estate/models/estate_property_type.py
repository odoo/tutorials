from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Group properties by type of building"
    _check_name = models.Constraint('UNIQUE(name)', 'This property type already exists')

    name = fields.Char(required=True)
