from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real E-state Property Tag"

    name = fields.Char(required=True)
