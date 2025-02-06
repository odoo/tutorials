from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Specific types of properties"

    name = fields.Char(string = "Name", required = True)
