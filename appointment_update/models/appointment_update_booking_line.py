from odoo import api, models, fields

class AppointmentBookingLine(models.Model):
    _inherit = "appointment.booking.line"

    appointment_resource_id = fields.Many2one('appointment.resource', string="Appointment Resource", ondelete="cascade", required=False)
    appointment_user_id = fields.Many2one('res.users', string="Appointment Update User", ondelete="cascade")

    @api.depends('appointment_resource_id.capacity', 'appointment_resource_id.shareable','appointment_type_id.track_capacity', 'capacity_reserved', 'appointment_type_id.total_booking')
    def _compute_capacity_used(self):
        self.capacity_used = 0
        for line in self:
            if line.capacity_reserved == 0:
                line.capacity_used = 0
            # my code changes
            elif line.appointment_type_id.track_capacity == 'multiple_booking_per_slot':
                line.capacity_used = 1
            elif line.appointment_type_id.schedule_based_on == 'resources' and (not line.appointment_resource_id.shareable or line.appointment_type_id.track_capacity == 'one_booking_per_slot'):
                line.capacity_used = line.appointment_resource_id.capacity
            else:
                line.capacity_used = line.capacity_reserved
