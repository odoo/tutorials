from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Specific tags for properties"

    name = fields.Char(string = "Name", required = True)
