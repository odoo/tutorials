from odoo import models, fields

class FreightTags(models.Model):
    _name = 'freight.tags'
    _description = 'Freight Tags'

    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
