from odoo import fields, models


class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag Model"

    name = fields.Char(required=True)
