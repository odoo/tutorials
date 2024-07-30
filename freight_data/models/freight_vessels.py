from odoo import fields, models


class FreightVessels(models.Model):
    _name = "freight.vessels"
    _description = "Freight Vessels Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
    vessel_owner_id = fields.Many2one(
        'res.partner',
        string='Vessel Owner',
        required=True
    )
