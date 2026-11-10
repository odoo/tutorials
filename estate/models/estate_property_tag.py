from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = 'name'
    _name_check = models.Constraint('UNIQUE(name)', "The name must be unique.")

    name = fields.Char(required=True)
    color = fields.Integer()
