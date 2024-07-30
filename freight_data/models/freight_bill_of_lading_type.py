from odoo import fields, models


class FreightContainerType(models.Model):
    _name = "freight.bill.lading.type"
    _description = "Freight Container Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
