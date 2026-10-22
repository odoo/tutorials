from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _check_name_unique = models.Constraint(
        'unique(name)',
        'Tag name must be unique.'
    )
