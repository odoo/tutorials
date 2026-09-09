from odoo import api, fields, models
from odoo.release import description

class MeetingReservation(models.Model):
    _name = "meeting.reservation"
    _description = "Meeting Reservation"
    _order = "start_time"

    name = fields.Char("Meeting Subject", required=True)
    building_id = fields.Many2one('meeting.building')
    room_ids = fields.One2many('meeting.room', string="Meeting Room", required=True)
    holder_id = fields.Many2one('res.users', string="Holder",
        required=True, default=lambda self: self.env.user)

    start_time = fields.Datetime("Start Time", required=True)
    end_time = fields.Datetime("End Time", required=True)

    state = fields.Selection([
                ("confirmed", "Confirmed"), ("canceled", "Canceled"),
            ], string="Status", default="confirmed", required=True, index=True)

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time < record.end_time:
                diff = record.end_time - record.start_time
                record.duration = round(diff.total_seconds() / 3600, 2)
            else:
                record.duration = 0

    def action_cancel(self):
        for record in self:
            record.write({"state": "canceled"})
            return True