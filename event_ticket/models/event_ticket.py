from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = ["event.event"] 

    tickets_per_registration = fields.Integer(
        string="Tickets per Registration",
        help="Number of tickets per registration",
        default=9
    )

    @api.constrains('tickets_per_registration', "event_ticket_ids")
    def _check_ticket_limit(self):
        for record in self:
            if record.tickets_per_registration < 1:
                raise ValidationError("Maximum tickets per registration must be at least 1.")
            for line in record.event_ticket_ids:
                if record.tickets_per_registration > line.seats_max:
                    raise ValidationError(f"You cannot book more than {line.seats_max} tickets.")
                