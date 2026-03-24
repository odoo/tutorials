from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate property tag"

    _order = 'name'

    name = fields.Char(required=True, string="Name")
    color = fields.Integer(string="Color")

    _name_unique_idx = models.UniqueIndex(
        '(name)',
        "The name of the property tag must be unique."
    )
