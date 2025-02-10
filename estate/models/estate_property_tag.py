from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order="name"

    name = fields.Char('Property tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
    ('estate_property_tag_name_unique', 'UNIQUE(name)', 'The tag must be unique.')]


