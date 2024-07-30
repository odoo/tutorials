from odoo import fields, models


class Flights(models.Model):
    _name = 'flights'
    _description = 'Flights Model'
    _inherits = {'freight.data': 'freight_type_id'}

    freight_type_id = fields.Many2one('freight.data')
    airline = fields.Many2one('res.partner', string='Airline')
