from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Specific tags for properties"

    name = fields.Char(string = "Name", required = True)
