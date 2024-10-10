from odoo import fields, models # type: ignore

class EstatePropertyTags(models.Model):

    _name = "estate.property.tags"
    _description = "Estate Property Tags Model"
    
    name = fields.Char(required=True)
   