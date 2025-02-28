from odoo import fields, models, api

class EventTicket(models.Model):
    _inherit = "event.event"

    set_max_ticket = fields.Integer(
        string="Set Max Registration Limit",
        compute="_compute_set_max_ticket",
        inverse="_inverse_set_max_ticket",
        store=False
    )

    @api.depends()
    def _compute_set_max_ticket(self):
        """Fetch the value from system parameters."""
        param_value = self.env["ir.config_parameter"].sudo().get_param("event.max_ticket_limit", default=10)
        for record in self:
            record.set_max_ticket = int(param_value)

    def _inverse_set_max_ticket(self):
        """Set the system parameter value when changed."""
        if self:
            self.env["ir.config_parameter"].sudo().set_param("event.max_ticket_limit", self.set_max_ticket)
