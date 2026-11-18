from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag'

    name = fields.Char('Tag', required=True)
