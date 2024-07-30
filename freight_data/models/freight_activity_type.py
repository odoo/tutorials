from odoo import fields, models


class FreightActivityType(models.Model):
    _name = "freight.activity.type"
    _description = "Freight Activity Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
