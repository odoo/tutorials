from odoo import fields, models

class EstateModel(models.Model):
    _name = "estate.property.tags"
    _description = "Estate/Property/Tags"

    name = fields.Char(required=True)
