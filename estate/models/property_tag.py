from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate property tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [('check_estate_property_tag_unique', 'UNIQUE (name)', "The name must be unique.")]
