from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name asc" 

    name = fields.Char("Tag name", required=True)
    color = fields.Integer("Color")
    