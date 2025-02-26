# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(
        string="Tickets per Registration",
        help="Number of tickets per registration. 0 means 9 ticket per registration.",
    )

    @api.constrains('tickets_per_registration')
    def _check_ticket_pre_registration(self):
        for record in self:
            if record.tickets_per_registration < 0:
                raise ValidationError(_("Ticket per registration cannot be negative."))
