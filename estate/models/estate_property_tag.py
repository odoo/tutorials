from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property_tag"
    _description = "Tags for property"
    name = fields.Char(string="name")
    _name_unique = models.UniqueIndex("(name)", "name must be unique")
