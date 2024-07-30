from odoo import models, fields


class FreightFlight(models.Model):
    _name = "freight.flight"
    _description = "this is freight flight"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    airline_id = fields.Many2one("res.partner", string="Airline")
    status = fields.Boolean(string='Status', default=True)
