from odoo import fields, models # type: ignore

class EstatePropertyTags(models.Model):

    _name = "estate.property.tags"
    _description = "Estate Property Tags Model"
    
    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'This property tag name already exists'),
    ]
   