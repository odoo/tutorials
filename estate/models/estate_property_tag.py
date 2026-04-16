from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property_tag"
    _description = "Tags for property"
    _order = "name"

    name = fields.Char(string="name")
    color = fields.Integer(default=0)

    _name_unique = models.UniqueIndex("(name)", "name must be unique")
