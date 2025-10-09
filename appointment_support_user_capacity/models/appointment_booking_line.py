from odoo import api, fields, models


class AppointmentBookingLine(models.Model):
    _inherit = "appointment.booking.line"

    appointment_user_id = fields.Many2one(
        "res.users",
        string="Staff User",
        help="The user who is handling this booking",
        ondelete="cascade",
    )
    appointment_resource_id = fields.Many2one(
        "appointment.resource",
        string="Appointment Resource",
        ondelete="cascade",
        required=False,
    )

    @api.depends(
        "appointment_resource_id.capacity",
        "appointment_resource_id.shareable",
        "appointment_type_id.capacity_type",
        "capacity_reserved",
        "appointment_type_id.user_capacity",
    )
    def _compute_capacity_used(self):
        self.capacity_used = 0
        for line in self:
            capacity_type = line.appointment_type_id.capacity_type
            if line.capacity_reserved == 0:
                line.capacity_used = 0
            elif capacity_type == "multiple_booking":
                line.capacity_used = 1
            elif capacity_type == "multiple_seats":
                line.capacity_used = line.capacity_reserved
            elif line.appointment_type_id.schedule_based_on == "resource":
                if (
                    not line.appointment_resource_id.shareable
                    or capacity_type == "one_booking"
                ):
                    line.capacity_used = line.appointment_resource_id.capacity
            else:
                line.capacity_used = line.capacity_reserved
