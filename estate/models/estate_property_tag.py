from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    name = fields.Char("Name", index=True, translate=True, required=True)
