from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentBookingLine(models.Model):
    _inherit = "appointment.booking.line"

    appointment_user_id = fields.Many2one('res.users', string="Appointment user", ondelete="cascade")
    appointment_resource_id = fields.Many2one('appointment.resource', string="Appointment Resource",ondelete="cascade",required=False)

    @api.depends(
        "appointment_resource_id.capacity",
        "appointment_resource_id.shareable",
        "appointment_type_id.capacity_type",
        "appointment_type_id.user_capacity_count",
        "capacity_reserved",
    )
    def _compute_capacity_used(self):
        self.capacity_used = 0
        for line in self:
            if line.capacity_reserved == 0:
                line.capacity_used = 0
            elif line.appointment_type_id.capacity_type == 'multiple_bookings':
                line.capacity_used = 1
            elif line.appointment_type_id.capacity_type == 'multiple_seats':
                line.capacity_used = line.capacity_reserved
            elif (not line.appointment_resource_id.shareable or line.appointment_type_id.capacity_type == 'single_booking') and line.appointment_type_id.schedule_based_on == 'resources':
                line.capacity_used = line.appointment_resource_id.capacity
            else:
                line.capacity_used = line.capacity_reserved
