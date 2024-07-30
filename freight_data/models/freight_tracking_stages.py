from odoo import fields, models


class FreightTrackingStages(models.Model):
    _name = "freight.tracking.stages"
    _description = "Freight Tracking Stages Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
