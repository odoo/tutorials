from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = "A property tag"

    name = fields.Char(string='Tag Name', required=True)
