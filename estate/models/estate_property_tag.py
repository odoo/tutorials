from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name asc"
    
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "The name of the property tag must be unique.")
    ]
    
    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color Index')
    property_ids = fields.Many2many('estate.property', 'property_tag_ids')


