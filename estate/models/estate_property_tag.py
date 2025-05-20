from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "used to add precision to a property"

    name = fields.Char(required=True)