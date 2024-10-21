from odoo import fields, models # type: ignore

class EstatePropertyTags(models.Model):

    _name = "estate.property.tags"
    _description = "Estate Property Tags Model"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer() 

    # Constraints
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'This property tag name already exists'),
    ]
   