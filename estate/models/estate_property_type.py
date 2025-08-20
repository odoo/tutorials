from odoo import models, fields


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type Model"

    name = fields.Char(required=True)
