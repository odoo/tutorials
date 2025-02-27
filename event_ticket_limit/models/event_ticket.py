from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_tickets_per_registration = fields.Integer(
        string="Tickets per Registration",
        help='Maximum Number of tickets per registration',
        default=7
    )
