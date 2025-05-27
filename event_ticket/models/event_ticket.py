from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(string="Tickets per Registration", default=1)

    _sql_constraints = [
        (
            "check_tickets_per_registration",
            "CHECK(tickets_per_registration >= 1)",
            "At least 1 ticket must be set per registration."
        )
    ]

    @api.constrains("tickets_per_registration", "seats_limited", "seats_max")
    def _check_tickets_per_registration(self):
        """Ensures tickets_per_registration does not exceed available seats if limited."""
        for record in self:
            if record.seats_limited and record.seats_max > 0 and record.tickets_per_registration > record.seats_max:
                raise ValidationError(
                    "You cannot set more tickets per registration than the available seats."
                )
