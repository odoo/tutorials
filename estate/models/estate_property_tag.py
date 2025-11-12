from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Real Estate Property Tag Model"
    _order = "name asc"

    name = fields.Char(required = True)
    color = fields.Integer()

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')]
