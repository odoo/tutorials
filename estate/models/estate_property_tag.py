from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Contains the different tags for properties"

    name = fields.Char(required=True)
