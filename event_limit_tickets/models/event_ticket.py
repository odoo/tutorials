from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = "event.event.ticket"
    
    max_tickets_allowed_per_registration = fields.Integer(
        string=_('Max Tickets Allowed Per Registration'),
        default=0,
        help=_("Maximum number of tickets allowed per registration of this ticket type. Set to 0 for unlimited.")
    )
    
    @api.constrains("max_tickets_allowed_per_registration", "seats_max")
    def _check_max_tickets_per_registration(self):
        for ticket in self:
            if ticket.max_tickets_allowed_per_registration < 0:
                raise ValidationError(_("Max Tickets Allowed Per Registration cannot be negative."))
            if ticket.seats_max > 0 and ticket.max_tickets_allowed_per_registration > ticket.seats_max:
                raise ValidationError(("Max Tickets Allowed Per Registration cannot exceed Maximum Attendees."))
            if ticket.seats_max == 0 and ticket.max_tickets_allowed_per_registration == 0:
                raise ValidationError(
                   _("Both Maximum Attendees and Max Tickets Allowed Per Registration cannot be set to 0 (unlimited). Please configure at least one limit.")
                )
