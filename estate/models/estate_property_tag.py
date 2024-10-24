from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Model representing the tags of each estate property'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', "This tag name already exists."),
    ]
