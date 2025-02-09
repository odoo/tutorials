from odoo import fields,models

class estatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "tags for the property"

    name = fields.Char("Property Tag", required=True)
