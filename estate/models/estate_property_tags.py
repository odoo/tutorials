from odoo import models, fields


class Estatetags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property tags'

    name = fields.Char(required=True)
