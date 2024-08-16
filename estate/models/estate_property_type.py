from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate property type"
    name = fields.Char('Title', required = True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type already exists!"),
    ]
