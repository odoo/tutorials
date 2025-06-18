from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "estate property type"
    _order = "id"

    name = fields.Char("Name", required=True)