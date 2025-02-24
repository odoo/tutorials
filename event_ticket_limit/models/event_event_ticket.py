from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InheritedEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    ticket_limit = fields.Integer(
        string="Ticket Limit",
        required=True,
        default=lambda self: self._get_default_ticket_limit()
    )

    @api.constrains('ticket_limit')
    def _check_ticket_limit(self):
        """Ensure ticket limit is greater than 0."""
        for ticket in self:
            if ticket.ticket_limit <= 0:
                raise ValidationError("Ticket limit must be greater than 0.")

    def _get_default_ticket_limit(self):
        """Fetch the default ticket limit from system parameters."""
        return int(self.env['ir.config_parameter'].sudo().get_param('event.ticket_limit_default', default=9))
