
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Event(models.Model):
    _inherit = "event.event"

    # Event-level limit for max tickets per registration
    default_tickets_per_registration = fields.Integer(
        string="Default Tickets per Registration",
        help="Maximum number of tickets that can be booked in a single registration for this event.",
        default=9
    )

    @api.constrains("default_tickets_per_registration")
    def _check_ticket_limit(self):
        for event in self:
            if event.default_tickets_per_registration < 0:
                raise ValidationError(
                    "Default tickets per registration must be greater than 0."
                )
