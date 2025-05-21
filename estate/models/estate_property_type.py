from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of an estate"

    name = fields.Char("Type", required=True)
