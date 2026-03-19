from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag Model'
    _order = 'name'


    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)', "A property tag name must be unique!"
    )
