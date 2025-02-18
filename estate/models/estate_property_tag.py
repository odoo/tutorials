from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this is the estate property tag model"
    name = fields.Char(required=True)
