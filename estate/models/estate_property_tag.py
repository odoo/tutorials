from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this model provides tags for estate property"
    name = fields.Char(required=True)
