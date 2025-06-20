from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    # misc
    name = fields.Char(required=True)