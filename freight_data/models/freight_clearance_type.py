from odoo import fields, models


class FreightClearanceType(models.Model):
    _name = "freight.clearance.type"
    _description = "Freight Clearance Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
