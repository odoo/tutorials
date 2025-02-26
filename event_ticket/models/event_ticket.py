from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(
        string="Tickets per Registration",
        help="Number of tickets per registration",
        width = "150px",
        default=9
    )

    @api.constrains('tickets_per_registration')
    def _check_ticket_limit(self):
        for record in self:
            if record.tickets_per_registration < 1:
                raise ValidationError("Maximum tickets per registration must be at least 1.")
            if record.tickets_per_registration > record.seats_max:
                raise ValidationError(f"You cannot book more than {record.seats_max} tickets.")
