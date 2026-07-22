from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    _name_idx = models.UniqueIndex('(name)', 'Another record already exists with the same name!')

    name = fields.Char(string='Name', required=True)
