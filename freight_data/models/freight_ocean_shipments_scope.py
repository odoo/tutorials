from odoo import fields, models


class FreightOceanShipmentsScope(models.Model):
    _name = "freight.ocean.shipments.scope"
    _description = "Freight Ocean Shipments Scope Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
