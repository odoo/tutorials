from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag assigned to property"

    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')

    name = fields.Char(string='Name', required=True)
