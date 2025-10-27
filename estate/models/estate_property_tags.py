from odoo import models, fields


class PropertyTypeTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
