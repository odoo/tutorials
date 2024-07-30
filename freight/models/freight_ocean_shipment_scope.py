from odoo import models, fields


class FreightOceanShipmentScope(models.Model):
    _name = "freight.ocean.shipment.scope"
    _description = "this is freight type"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
