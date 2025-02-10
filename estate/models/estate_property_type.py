from odoo import models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model for property types"

    name = fields.Char(required=True)
