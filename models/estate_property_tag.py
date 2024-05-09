from odoo import fields, models


class Tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags propiedades'

    name = fields.Char('Nombre', required=True)
