from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = "Property Tags"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
