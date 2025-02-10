from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Different Tags to describe the aesthetics of Property"
    
    name = fields.Char('Property Tag', required = True)