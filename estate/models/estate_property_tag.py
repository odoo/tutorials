from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'The Property tag should be unique')]
