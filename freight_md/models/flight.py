from odoo import models, fields


class Flight(models.Model):
    _name = 'flight'
    _description = 'Flight'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    airline_id = fields.Many2one('res.partner', string='Airline')
    status = fields.Boolean(string='Status', default=True)
