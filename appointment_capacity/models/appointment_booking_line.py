from odoo import api, models,fields

class AppointmentBookingLine(models.Model):
    _inherit = "appointment.booking.line"

    appointment_user_id = fields.Many2one('res.users', string="Appointment User", ondelete="cascade")
    appointment_resource_id = fields.Many2one('appointment.resource', string="Appointment Resource", ondelete="cascade",required=False)

    @api.depends('appointment_resource_id.capacity', 'appointment_resource_id.shareable',
                'appointment_type_id.resource_capacity', 'capacity_reserved','appointment_type_id.capacity_count')
    def _compute_capacity_used(self):
        self.capacity_used = 0
        for line in self:
            if line.capacity_reserved == 0:
                line.capacity_used = 0
            elif line.appointment_type_id.resource_capacity == 'multi_booking':
                line.capacity_used = 1
            elif line.appointment_type_id.schedule_based_on == 'resources' and (not line.appointment_resource_id.shareable or line.appointment_type_id.resource_capacity == 'one_booking'):
                line.capacity_used = line.appointment_resource_id.capacity
            else:
                line.capacity_used = line.capacity_reserved
