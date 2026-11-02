from odoo import models, fields


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(string="Title", required=True)
