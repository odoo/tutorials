from odoo import models, api, fields
from odoo.exceptions import ValidationError


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Estate Property Visit"

    name = fields.Char()
    customer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    agent_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    visit_date = fields.Datetime(required=True)

    status_visit = fields.Selection([
        ('schedule', "Scheduled"),
        ('done', "Done"),
        ('cancel', "Cancel"),
    ], string="Status", readonly=True, default="schedule")

    @api.constrains("visit_id", "agent_id")
    def _check_clash(self):
        for record in self:
            clash = self.search([
                ('agent_id', '=', record.agent_id.id),
                ('visit_date', '=', record.visit_date),
                ('id', '!=', record.id)
            ])

            if clash:
                raise ValidationError("Agent is not available for this time, as he already has another visit scheduled")

    def action_cancel(self):
        self.status_visit = "cancel"
    
    def action_done(self):
        self.status_visit = "done"
