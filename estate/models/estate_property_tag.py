from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "estate property tags"

    # simple fields
    name = fields.Char("Tag Name", required=True)
    
        #sql constraints
    _sql_constraints = [
        ('check_unique_tag_name', 'UNIQUE(name)',
         'The tag name must be unique'),
    ]
