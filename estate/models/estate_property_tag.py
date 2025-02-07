from odoo import models, fields


class estate_property_tag(models.Model):
    _name = "estate_property.tag"
    _description = "estate property tag"
    _order = "name asc" 

    name = fields.Char("Tag name", required=True)
    color = fields.Integer("Color")
    