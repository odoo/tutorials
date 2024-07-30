from odoo import models, fields


class Flights(models.Model):
    _name = "flights"
    _description = "Flights"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    airline_id = fields.Many2one('res.partner', string='Airline', required=True)
    status = fields.Boolean(string='Status', default=True)
