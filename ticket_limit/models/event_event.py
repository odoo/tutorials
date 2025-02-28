from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EventEvent(models.Model):
    _inherit = 'event.event'

    default_registration_tickets = fields.Integer(string="Default Registration Tickets", default=1)

    @api.constrains('default_registration_tickets')
    def _check_default_registration_tickets(self):
        for record in self:
            if record.default_registration_tickets <= 0:
                raise ValidationError("At least 1 ticket must be set per registration.")
