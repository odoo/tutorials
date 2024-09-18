from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name"

    name = fields.Char("Name", index=True, translate=True)
