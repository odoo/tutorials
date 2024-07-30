from odoo import fields, models


class PackageType(models.Model):
    _name = 'package.type'
    _description = 'Package Type Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
    transport_modes = fields.Selection([
        ('air', 'Air'),
        ('lcr', 'LCR'),
    ], string='Is:', required=True)
