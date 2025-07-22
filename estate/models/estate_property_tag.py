from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for Properties"
    _order = "name"
    _sql_constraints = [("name_uniq", "UNIQUE(name)", "Tag name must be unique")]
    
    name = fields.Char(required=True)
    color = fields.Integer("Color Index")