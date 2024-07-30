from odoo import models, fields


class OceanShipmentsScope(models.Model):
    _name = "ocean.shipments.scope"
    _description = "Ocean Shipments Scope"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
