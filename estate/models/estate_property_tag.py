from odoo import models, fields


class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required=True)
