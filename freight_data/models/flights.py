from odoo import fields, models


class Flights(models.Model):
    _name = 'flights'
    _description = 'Flights Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
    airline = fields.Many2one('res.partner', string='Airline')