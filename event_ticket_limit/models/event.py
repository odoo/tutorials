from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    default_tickets_per_registration = fields.Integer(
        string="Default Tickets per Registration",
        default=10,
        help="Defines the maximum number of tickets per registration.",
        required=True
    )
