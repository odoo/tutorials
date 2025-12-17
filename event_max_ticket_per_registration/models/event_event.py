from odoo import api, models, fields
from odoo.exceptions import ValidationError


class EventType(models.Model):
    _inherit = "event.event"

    has_ticket_limitation = fields.Boolean(string="Limit Tickets per Rgistration", default=False)
    ticket_max_per_registration = fields.Integer(compute='_compute_tickets_max_per_registration',
        readonly=False, store=True, default=0,
        help="It will select this default maximum value when you choose number of tickets in this event registration")

    @api.depends('has_ticket_limitation')
    def _compute_tickets_max_per_registration(self):
        for record in self:
            if not record.has_ticket_limitation:
                record.ticket_max_per_registration = 0

    @api.constrains("ticket_max_per_registration")
    def _set_ticket_max_per_registration(self):
        for record in self:
            if record.has_ticket_limitation and record.ticket_max_per_registration == 0:
                raise ValidationError("Limit Tickets should be greater than 0")
