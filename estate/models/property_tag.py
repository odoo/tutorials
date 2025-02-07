from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tags"
    name = fields.Char("Name")
