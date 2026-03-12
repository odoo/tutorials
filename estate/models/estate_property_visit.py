from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Property Visit"

    name = fields.Char(string="Visit Name")
    property_id = fields.Many2one("estate.property", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer")
    agent_id = fields.Many2one(
        "res.users",
        string="Agent",
        required=True
    )
    visit_date = fields.Datetime(string="Visit Date")

    state = fields.Selection([
        ('schedule', 'Scheduled'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default="schedule")

    

    @api.constrains('property_id', 'visit_date')
    def _check_visit_time(self):
        for rec in self:
            if not rec.property_id or not rec.visit_date:
                continue

            existing = self.search([
                ('id', '!=', rec.id),
                ('property_id', '=', rec.property_id.id),
                ('visit_date', '=', rec.visit_date),
                ('state', '=', 'schedule')
            ])

            if existing:
                raise ValidationError(
                    "Another visit is already scheduled for this property at the same time."
                )
