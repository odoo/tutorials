from datetime import datetime

import pytz
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.osv.expression import combine


class MeetingReservation(models.Model):
    _name = "meeting.reservation"
    _description = "Meeting Reservation"
    _order = "start_time"

    name = fields.Char("Meeting Subject", required=True)
    description = fields.Text("Description")

    building_id = fields.Many2one(
        "meeting.building",
        string="Building",
        related="room_id.building_id",
        index=True,
    )
    room_id = fields.Many2one(                                                                                                                       
            'meeting.room',                                                                                                                              
            string="Meeting Room",                                                                                                                       
            required=True,                                                                                                                               
            domain="[('active', '=', True)]",                                                                                                            
            group_expand='_read_group_room_ids',                                                                                                         
        )
    organizer_id = fields.Many2one('res.users', string="Holder",
        required=True, default=lambda self: self.env.user)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="room_id.company_id",
        readonly=True,
        index=True,
    )
    meeting_date = fields.Date(
        "Meeting Date",
        compute="_compute_meeting_date",
        inverse="_inverse_meeting_date",
        store=False,
        default=fields.Date.context_today,
    )
    start_time = fields.Datetime("Start Time", required=True)
    end_time = fields.Datetime("End Time", required=True)

    capacity = fields.Integer("Room Capacity", related="room_id.seating_capacity", readonly=True)

    duration = fields.Float("Duration (hours)",
        compute="_compute_duration", store=True)
    
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("canceled", "Canceled"),
    ], string="Status", default="draft", required=True, index=True)

    @api.model                                                                                                                                       
    def _read_group_room_ids(self, rooms, domain, order):                                                                                            
        return rooms.search([('active', '=', True)], order=order)  

    @api.constrains("start_time")
    def _compute_meeting_date(self):
        for record in self:
            record.meeting_date = record.start_time.date() if record.start_time else False

    @api.onchange("meeting_date")
    def _onchange_meeting_date(self):
        if self.meeting_date:
            if self.start_time:
                self.start_time = datetime.combine(self.meeting_date, self.start_time.time())
            if self.end_time:
                self.end_time = datetime.combine(self.meeting_date, self.end_time.time())

    def _inverse_meeting_date(self):
        for record in self:
            if record.meeting_date:
                if record.start_time:
                    record.start_time = datetime.combine(record.meeting_date, record.start_time.time())
                if record.end_time:
                    record.end_time = datetime.combine(record.meeting_date, record.end_time.time())
    
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
        for record in self:
            if record.start_time and record.end_time and record.start_time >= record.end_time:
                raise ValidationError(_("Start time must be before end time."))

    @api.constrains("start_time", "end_time", "room_id")
    def _check_working_hours(self):
        # Meeting must fall within the building's working hours.
        for record in self:
            if not (record.room_id and record.start_time and record.end_time):
                continue
            building = record.room_id.building_id
            if not building:
                continue

            if building.resource_calendar_id:
                calendar = building.resource_calendar_id
                start_utc = record.start_time if record.start_time.tzinfo else record.start_time.replace(tzinfo=pytz.UTC)
                end_utc = record.end_time if record.end_time.tzinfo else record.end_time.replace(tzinfo=pytz.UTC)
                
                intervals = calendar._work_intervals_batch(start_utc, end_utc).get(False, [])

                total_work_seconds = sum((stop - start).total_seconds() for start, stop,_meta in intervals)
                meeting_seconds = (record.end_time - record.start_time).total_seconds()
                if total_work_seconds < meeting_seconds:
                    raise ValidationError(
                        _(
                            "The reservation for room '%(room)s' falls outside building working hours or during a scheduled closure/holiday."
                        )
                        % {"room": record.room_id.code}
                    )
            elif building.working_time_start or building.working_time_end:
                start_float = record.start_time.hour + record.start_time.minute / 60.0
                end_float = record.end_time.hour + record.end_time.minute / 60.0
                start_str = f"{int(building.working_time_start):02d}:{int(round((building.working_time_start % 1) * 60)):02d}"
                end_str = f"{int(building.working_time_end):02d}:{int(round((building.working_time_end % 1) * 60)):02d}"

                if (
                    record.start_time.date() != record.end_time.date()
                    or start_float < building.working_time_start
                    or end_float > building.working_time_end
                ):
                    raise ValidationError(
                    _(
                        "Meeting time for room '%(room)s' must be within building working hours "
                        "(%(start)s - %(end)s UTC)."
                    ) % {
                        "room": record.room_id.code,
                        "start": start_str,
                        "end": end_str,
                    }
                    )
    
    @api.constrains("room_id", "start_time", "end_time", "state")
    def _check_no_overlap(self):
        for record in self:
            if record.state != "confirmed" or not record.start_time or not record.end_time:
                continue
            domain = [
                ("room_id", "=", record.room_id.id),
                ("state", "=", "confirmed"),
                ("start_time", "<", record.end_time),
                ("end_time", ">", record.start_time),
            ]
            record_id = record._origin.id if record._origin else record.id
            if record_id:
                domain.append(("id", "!=", record_id))        

            overlap = self.search(domain, limit=1)
            if overlap:
                raise ValidationError(
                    _(
                        "Room '%(room)s' is already booked from %(start)s to %(end)s."
                    )
                    % {
                        "room": record.room_id.code,
                        "start": overlap.start_time,
                        "end": overlap.end_time,
                    }
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