from odoo import api, fields, models
from odoo.exceptions import UserError


class EventEvent(models.Model):
    _inherit = 'event.event'

    tickets_limited = fields.Boolean(string="Ticket Limit", default=False)
    max_ticket = fields.Integer(string="Tickets per Registration", default=9)

    @api.constrains('max_ticket')
    def _check_max_ticket(self):
        for record in self:
            if record.tickets_limited:
                if record.max_ticket == 0:
                    raise UserError("Maximum tickets must be grater than 0!!!")
