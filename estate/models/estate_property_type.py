from odoo import fields, models 

class EstatePropertyType(models.Model): 
    _name = "estate.property.type"
    _description = "Type of a Property"
    _sql_constraints = [("name_uniq", "UNIQUE(name)", "Property type name must be unique")]
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")