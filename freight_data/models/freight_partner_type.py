from odoo import fields, models


class FreightPartnerType(models.Model):
    _name = "freight.partner.type"
    _description = "Freight Partner Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
