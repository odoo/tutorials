from odoo import fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'stores property tags'

    name = fields.Char('Name', required=True)
