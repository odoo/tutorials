from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.tag'
    _description = 'Model representing the tags of each estate property'

    name = fields.Char(string="Name", required=True)
