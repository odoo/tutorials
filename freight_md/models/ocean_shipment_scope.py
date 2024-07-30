from odoo import fields, models


class OceanShipmentScope(models.Model):
    _name = 'ocean.shipment.scope'
    _description = 'Ocean Shipment Scope'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
