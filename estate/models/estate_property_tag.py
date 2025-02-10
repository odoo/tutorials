from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order="name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color", default=0)
