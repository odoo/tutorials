from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RoomAvailability(models.Model):
    _name = 'room.availability'
    _description = ''

    room_id = fields.Many2one('room.room', string='Room')
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)

    @api.constrains('start_time', 'end_time')
    def _check_time_validity(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError('Start Time must be earlier than End Time.')
            if not (0 <= record.start_time.hour <= 23):
                raise ValidationError('Start Time must be between 0:00 and 23:59.')
            if not (0 <= record.end_time.hour <= 23):
                raise ValidationError('End Time must be between 0:00 and 23:59.')

    @api.constrains('start_time', 'end_time', 'room_id')
    def _check_time_overlapping(self):
        for record in self:
            overlap = self.search([
                ('room_id', '=', record.room_id.id),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time)
            ])
            if overlap:
                raise ValidationError('There is an overlapping availability for this room.')
