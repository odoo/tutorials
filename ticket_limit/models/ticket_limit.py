from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    tickets_per_registration = fields.Integer(string="Tickets per Registration",default=1)

    @api.constrains("tickets_per_registration")
    def _check_tickets_per_registration(self):
        for record in self:
            if record.tickets_per_registration <= 0:
                raise ValidationError("At least 1 ticket must be set per registration.")

class EventEvent(models.Model):
    _inherit = 'event.event'

    default_registration_tickets = fields.Integer(string="Default Registration Tickets",default=1)

    @api.constrains("buy_tickets")
    def _check_default_registration_tickets(self):
        for record in self:
            if record.default_registration_tickets <= 0:
                raise ValidationError("At least 1 ticket must be set per registration.")
