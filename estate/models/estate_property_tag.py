from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description ="It defines the estate property tags"
    _order="name asc"

    name= fields.Char(required=True)
    color= fields.Integer(string='Color')
