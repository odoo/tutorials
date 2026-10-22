from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of properties"

    name = fields.Char(required=True)
    _check_type_name = models.Constraint("UNIQUE(name)", "Type names must be unique.")
    _order = 'name asc'
    
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
