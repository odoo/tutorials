from odoo import fields, models


class Event(models.Model):
    _inherit = "event.event"

    default_tickets_per_registration = fields.Integer(
        string=" Default Tickets per Registration",
        help='Maximum Number of tickets per registration',
        default=7
    )
