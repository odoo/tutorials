from odoo import models, fields 


class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    max_register = fields.Integer(
        string='Max Registrations Per User',
        default=1,
        help="Maximum number of registrations allowed per user for this ticket."
    )
