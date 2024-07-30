from odoo import fields, models


class FreightFlights(models.Model):
    _name = "freight.flights"
    _description = "Freight Flights Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    airline_id = fields.Many2one(
        'res.partner',
        string='Airline',
        required=True
    )
