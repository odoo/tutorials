from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Contains the different tags for properties"
    _check_name_is_unique = models.Constraint('UNIQUE(name)')
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
