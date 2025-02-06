from odoo import fields, models

class EstatePropertyTg(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)