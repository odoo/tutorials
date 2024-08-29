from odoo import fields, models

class EstatePropertyTag(models.Model):
    # model definition
    _name = "estate.property.tag"
    _description = "property tag model"

    # normal fields
    name = fields.Char(required=True)
