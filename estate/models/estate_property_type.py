from odoo import fields, models



class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"


    name = fields.Char('Property Type', required=True)
   
    _sql_constraints = [
    ('estate_property_type_name_unique', 'UNIQUE(name)', 'The property type must be unique.')]
