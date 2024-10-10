from odoo import models, fields # type: ignore

class estatePropertyTag(models.Model):
    
    _name = "estate.property.tag"
    _description = "This is property Tag model"

    name = fields.Char(required=True, string="Tag")