from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property_tag"
    name = fields.Char(string="name")
