from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MeetingReservation(models.Model):
    _name = "meeting.reservation"
    _description = "Meeting Reservation"
    _order = "start_time"

    name = fields.Char("Meeting Subject", required=True)
    building_id = fields.Many2one('meeting.building')
    room_id = fields.Many2one('meeting.room', string="Meeting Room", required=True)
    organizer_id = fields.Many2one('res.users', string="Holder",
        required=True, default=lambda self: self.env.user)

    start_time = fields.Datetime("Start Time", required=True)
    end_time = fields.Datetime("End Time", required=True)

    start_date = fields.Date(
        "Start Date", compute="_compute_start_parts",
        inverse="_inverse_start_parts", store=False)
    start_hour = fields.Float(
        "Start Hour", compute="_compute_start_parts",
        inverse="_inverse_start_parts", store=False)

    end_date = fields.Date(
        "End Date", compute="_compute_end_parts",
        inverse="_inverse_end_parts", store=False)
    end_hour = fields.Float(
        "End Hour", compute="_compute_end_parts",
        inverse="_inverse_end_parts", store=False)

    duration = fields.Float("Duration (hours)",
        compute="_compute_duration", store=True)
    description = fields.Text("Description")

    state = fields.Selection([
                ("draft", "Draft"),
                ("confirmed", "Confirmed"),
                ("canceled", "Canceled"),
            ], string="Status", default="draft", required=True, index=True)

    @api.depends("start_time")
    def _compute_start_parts(self):
        for record in self:
            if record.start_time:
                record.start_date = record.start_time.date()
                record.start_hour = record.start_time.hour + record.start_time.minute / 60.0
            else:
                record.start_date = False
                record.start_hour = 0.0

    @api.depends("end_time")
    def _compute_end_parts(self):
        for record in self:
            if record.end_time:
                record.end_date = record.end_time.date()
                record.end_hour = record.end_time.hour + record.end_time.minute / 60.0
            else:
                record.end_date = False
                record.end_hour = 0.0

    def _inverse_start_parts(self):
        for record in self:
            if record.start_date:
                s_hour = int(record.start_hour or 0.0)
                s_minute = int(round(((record.start_hour or 0.0) - s_hour) * 60))
                record.start_time = datetime.combine(
                    record.start_date, datetime.min.time()
                ).replace(hour=s_hour, minute=s_minute)

    def _inverse_end_parts(self):
        for record in self:
            if record.end_date:
                e_hour = int(record.end_hour or 0.0)
                e_minute = int(round(((record.end_hour or 0.0) - e_hour) * 60))
                record.end_time = datetime.combine(
                    record.end_date, datetime.min.time()
                ).replace(hour=e_hour, minute=e_minute)
                
    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time and (record.start_time < record.end_time):
                diff = record.end_time - record.start_time
                record.duration = round(diff.total_seconds() / 3600, 2)
            else:
                record.duration = 0

    @api.constrains("start_time", "end_time")
    def _check_times(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.start_time >= rec.end_time:
                raise ValidationError("Start time must be before end time.")

    @api.constrains("start_time", "end_time", "room_id")
    def _check_working_hours(self):
        """Meeting must fall within the building's working hours."""
        for rec in self:
            if rec.room_id and rec.room_id.building_id and rec.start_time and rec.end_time:
                building = rec.room_id.building_id
                start_float = rec.start_time.hour + rec.start_time.minute / 60.0
                end_float = rec.end_time.hour + rec.end_time.minute / 60.0
                if (start_float < building.working_time_start
                        or end_float > building.working_time_end):
                    raise ValidationError(
                        "Meeting time must be within building working hours "
                        "(%s - %s UTC)." % (
                            building.working_time_start,
                            building.working_time_end,
                        )
                    )

    @api.constrains("room_id", "start_time", "end_time", "state")
    def _check_no_overlap(self):
        """No two confirmed meetings can overlap in the same room."""
        for record in self:
            if record.state != "confirmed" or not record.start_time or not record.end_time:
                continue
            overlap = self.search([
                ("id", "!=", record.id),
                ("room_id", "=", record.room_id.id),
                ("state", "=", "confirmed"),
                ("start_time", "<", record.end_time),
                ("end_time", ">", record.start_time),
            ], limit=1)
            if overlap:
                raise ValidationError(
                    "Room '%s' is already booked from %s to %s."
                    % (record.room_id.code, overlap.start_time, overlap.end_time)
                )

    def action_cancel(self):
        for record in self:
            is_manager = self.env.user.has_group('hr.group_hr_manager')
            is_owner = record.organizer_id ==self.env.user

            if not (is_manager or is_owner):
                raise UserError(_("You can only cancel your own meetings."))
                if record.state == 'canceled':
                    raise UserError(_("This meeting is already canceled."))

            record.write({"state": "canceled"})
        return True

    def action_confirm(self):
        if not self.env.user.has_group('hr.group_hr_manager'):
            raise UserError(_("Only managers can confirm meetings."))
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft meetings can be confirmed."))

            record.write({"state": "confirmed"})
            return True