from odoo import fields, models


class Events(models.Model):
    _inherit = 'event.event.ticket'

    ticket_registration_limit = fields.Integer(string="Ticket Registration Limit", default=7)
