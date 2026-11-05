from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstateVisitor(models.Model):
    _name = "estate.visitor"
    _description = "Estate Property Visitor"

    visit_id = fields.Many2one("res.partner", string="Visitor", required=True)
    event_id = fields.Many2one("calendar.event", string="Calender Event")
    start_date_time = fields.Datetime("Appointment Time", required=True)
    end_date_time = fields.Datetime(compute="_compute_end_date_time", store=True)
    stage = fields.Selection(
        [("schedule", "Schedule"), ("visited", "Visited")], default="schedule"
    )
    property_id = fields.Many2one("estate.property", required=True, readonly=True)

    @api.depends("start_date_time")
    def _compute_end_date_time(self):
        self.end_date_time = self.start_date_time + relativedelta(hours=1)

    @api.constrains("start_date_time")
    def _check_appointment(self):
        for rec in self:
            overlap = rec.search_count(
                [
                    ("id", "!=", rec.id),
                    ("property_id", "=", rec.property_id.id),
                    (
                        "start_date_time",
                        "<",
                        rec.start_date_time + relativedelta(hours=1),
                    ),
                    ("end_date_time", ">", rec.start_date_time),
                ],
                limit=1,
            )
            if overlap:
                raise ValidationError("Time solt is already booked")

    @api.model_create_multi
    def create(self, vals_list):
        visitors = super().create(vals_list)

        for visitor in visitors:
            event = self.env["calendar.event"].create(
                {
                    "name": f"Property Visit -{visitor.property_id.name}",
                    "start": visitor.start_date_time,
                    "stop": visitor.end_date_time,
                    "user_id": self.env.user.id,
                    "partner_ids": [
                        (4, self.env.user.partner_id.id),
                        (4, visitor.visit_id.id),
                    ],
                }
            )
            visitor.event_id = event.id

        return visitors
