from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tags'
    _order = 'name'
    _sql_constraints = [
        ('check_name_uniquness', 'UNIQUE(name)', 'Property type must be unique.')
    ]

    name = fields.Char(required=True)
    color = fields.Integer("Color Index", default=0)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_tag_id', string="Properties")
