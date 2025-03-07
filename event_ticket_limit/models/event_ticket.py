from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    ticket_limit = fields.Integer(
        string="Tickets per Registration",
        default=lambda self: self._get_default_tickets_per_registration()
    )

    def _get_default_tickets_per_registration(self):
        """Fetch the default ticket limit from the related event."""
        return self.event_id.default_tickets_per_registration if self.event_id else 7

    @api.constrains('ticket_limit')
    def _check_ticket_limit(self):
        for ticket in self:
            if ticket.ticket_limit <= 0 :
                raise ValidationError("ticket limit for event should be greater than 0")
