from odoo import models, fields
class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string="Tag Name", required=True)
    tag_ids = fields.Many2many(
        'estate.property.tag',
        'estate_property_tag_rel',  
        'tag_id1',  
        'tag_id2',
        string="Related Tags"
    )
    
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'The tag name must be unique.')
    ]
