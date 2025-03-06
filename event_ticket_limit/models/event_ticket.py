from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    ticket_limit = fields.Integer(
        string="Tickets per Registration",
        help="Maximum number of tickets per registration",
        default=lambda self: self._get_default_tickets_per_registration()
    )

    def _get_default_tickets_per_registration(self):
        """Fetch the default ticket limit from the related event."""
        return self.event_id.default_tickets_per_registration if self.event_id else 7
