from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Defines the property tags'

    name = fields.Char('Name', required=True)
