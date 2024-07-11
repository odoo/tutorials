from odoo import models, fields


class estate_tags(models.Model):
    _name = "estate.property.tags"
    _description = "This is Real Estate property tags"
    _order = "name"

    name = fields.Char("Tags", required=True)
    color = fields.Integer("color")

    _sql_constraints = [('check_property_tags', 'unique(name)', 'The property tags must be unique.')]
