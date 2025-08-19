from odoo import models, fields

class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag Model"

    name = fields.Char(required=True)