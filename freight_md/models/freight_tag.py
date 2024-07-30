from odoo import models, fields


class FreightTag(models.Model):
    _name = 'freight.tag'
    _description = 'Freight Tags'

    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
