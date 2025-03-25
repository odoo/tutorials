# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    max_tickets_per_registration = fields.Integer(
        string="Max Tickets Per Registration",
        help="Defines the maximum number of tickets allowed per registration. "
             "Set 0 to ignore this rule set as unlimited."
    )

    @api.constrains('max_tickets_per_registration')
    def _check_max_tickets_per_registration(self):
        for ticket in self:
            if ticket.max_tickets_per_registration < 0:
                raise ValidationError(_("Max Tickets Per Registration must be greater than 0."))
