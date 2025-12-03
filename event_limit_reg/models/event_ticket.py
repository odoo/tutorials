from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_registration_per_user_limit = fields.Integer(
        string="Tickets limit per user",
        help="maximum number of tickets that a single user can book for this event",
    )
