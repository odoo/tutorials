from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ticket_limit_default = fields.Integer(
        string="Default Ticket Limit Per Registration",
        config_parameter="event.ticket_limit_default",
        default=9
    )

    @api.constrains('ticket_limit_default')
    def _check_ticket_limit_default(self):
        for record in self:
            if record.ticket_limit_default <= 0:
                raise ValidationError("The default ticket limit must be greater than 0.")
