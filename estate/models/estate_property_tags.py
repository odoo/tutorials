from odoo import fields, models


class property_tags(models.Model):
    _name = "estate.property.tags"
    _description = "Model to modelize Tags of Properties"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The Tag\'s name must be unique.')
    ]
