from odoo import fields, models


class Type(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipos de propiedades'

    name = fields.Char('Nombre', required=True)
