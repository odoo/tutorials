from odoo import fields, models


class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    maximum_tickets_per_registration = fields.Integer(
        string="Maximum Tickets Per Registration",
        help="Define the maximum numbers of tickets allowed to book per registration."
    )
