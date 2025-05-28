from odoo import fields, models


class EstateTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'It allows to create a new property tag'
    _order = 'name desc'

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    _sql_constraints = [('unique_tag_by_estate_property', 'UNIQUE(name)', 'Only one name by tag')]
