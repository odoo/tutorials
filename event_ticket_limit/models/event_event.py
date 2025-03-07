from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Event(models.Model):
    _inherit = "event.event"

    default_tickets_per_registration = fields.Integer(
        string="Default Tickets per Registration",
        help='Maximum Number of tickets per registration',
        default=7
    )

    @api.constrains('default_tickets_per_registration')
    def _check_ticket_limit(self):
        for event in self:
            if event.default_tickets_per_registration <= 0 :
                raise ValidationError("default tickets per registration for event should be greater than 0")
