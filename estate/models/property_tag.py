from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag assigned to property"
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')