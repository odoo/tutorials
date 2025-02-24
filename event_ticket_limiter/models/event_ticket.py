from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EventTicket(models.Model):
    _inherit="event.event.ticket"
    
    _sql_constraints = [
        ("check_max_tickets_per_registration", "CHECK(max_tickets_per_registration >= 1)", "At least 1 ticket must be set per registration.")
    ]
    
    max_tickets_per_registration = fields.Integer(
        string="Max Tickets Per Registration",
        help="Set the maximum number of tickets a user can purchase per registration from website.",
        default=1
    )
    
    @api.constrains("max_tickets_per_registration", "seats_limited", "seats_max")
    def _check_max_tickets_per_registration(self):
        """Ensures max_tickets_per_registration does not exceed available seats if limited."""
        for record in self:
            if record.seats_limited and record.max_tickets_per_registration > record.seats_max:
                raise ValidationError("Max tickets per registration cannot exceed available seats.")
