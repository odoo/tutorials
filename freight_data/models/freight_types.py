from odoo import fields, models


class FreightFreightType(models.Model):
    _name = "freight.type"
    _description = "Freight Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
