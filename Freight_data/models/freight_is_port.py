from odoo import models, fields

class FreightIsPort(models.Model):
    _name = 'freight.is.port'
    _description = 'Port Options'

    name = fields.Char(string='Name', required=True)
