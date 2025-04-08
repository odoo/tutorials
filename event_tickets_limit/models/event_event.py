from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    max_tickets_per_registration = fields.Integer(
        string="Max Tickets Per Registration",
        default=9,
        help="The maximum number of tickets that can be booked in a single registration."
    )
