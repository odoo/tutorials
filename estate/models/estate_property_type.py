from odoo import models, fields


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of the property ..."

    name = fields.Char("Name")
