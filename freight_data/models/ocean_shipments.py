from odoo import fields, models


class OceanShipments(models.Model):
    _name = 'ocean.shipments'
    _description = 'Ocean Shipments Scope Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
