from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag assigned to property"

    name = fields.Char(string='Name', required=True)
