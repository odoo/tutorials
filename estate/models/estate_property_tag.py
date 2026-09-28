from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Tags for estate properties"
    _order = 'name'

    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="Color")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        "Each property tag should have a unique name."
    )
