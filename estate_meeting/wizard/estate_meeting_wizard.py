from odoo import fields, models
from odoo.http import request


class ScheduleMeeting(models.TransientModel):
    _name = "estate.meeting.wizard"
    _description = "Scheduled meeting"

    agenda = fields.Text(string="Agenda")
    start_date = fields.Datetime(
        "Start",
        required=True,
    )
    end_date = fields.Datetime("Stop", required=True, readonly=False)
    description = fields.Text(string="Description")

    def action_confirm(self):
        context = self.env.context
        active_ids = context.get("active_ids", [])
        properties = request.env["estate.property"].sudo().browse(active_ids)

        for properties in properties:
            salesman = properties.salesman_id
        self.env["calendar.event"].create(
            {
                "name": self.agenda,
                "start": self.start_date,
                "stop": self.end_date,
                "description": self.description,
                "partner_ids": [(6, 0, [salesman.partner_id.id])],
            }
        )
