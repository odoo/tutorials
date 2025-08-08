from odoo import api, fields, models
from odoo.exceptions import ValidationError

"""
This module handles meeting room booking functionalities.
"""

class MeetingRoomBooking(models.Model):
    _name = 'meeting.booking'
    _description = 'Meeting Room Booking'

    name = fields.Char(string='Booking Reference', required=True, default='New')
    room_id = fields.Many2one(comodel_name='meeting.room', string='Room', required=True)
    start_time = fields.Datetime(string='Start Time',required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    booked_by = fields.Many2one(comodel_name='res.users', string='Booked by', default=lambda self: self.env.user)

    @api.constrains('start_time', 'end_time', 'room_id')
    def _check_double_booking(self):
        for booking in self:
            if booking.start_time >= booking.end_time:
                raise ValidationError('Start Time must be less than End Time.')
            
            overlapping_bookings = self.search([
                ('room_id', '=', booking.room_id.id),
                ('id', '!=', booking.id),
                ('start_time', '<', booking.end_time),
                ('end_time', '>', booking.start_time)
            ])
            if overlapping_bookings:
                raise ValidationError('The selected room is already booked for the specified time.')