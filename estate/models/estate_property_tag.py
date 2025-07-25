from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char('Property tag', required=True)

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'The Property tag should be unique')]
