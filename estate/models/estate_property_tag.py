from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property tag"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _name_constraint = models.UniqueIndex('(name)', "Tag names must be unique.")
