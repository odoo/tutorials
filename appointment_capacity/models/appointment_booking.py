from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentBookingLine(models.Model):
    _inherit = "appointment.booking.line"

    appointment_user_id = fields.Many2one('res.users', string="Appointment user", ondelete="cascade")
    
    appointment_resource_id = fields.Many2one('appointment.resource', string="Appointment Resource",
        ondelete="cascade",required=False)
    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     """ Override fields_get to dynamically remove the 'required' constraint from 'appointment_resource_id'. """
    #     res = super().fields_get(allfields, attributes)
    #     print("hkjsdhuih")
    #     if 'appointment_resource_id' in res:
    #         res['appointment_resource_id']['required'] = False
    #     return res
    
    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     """ Hide first and last name field if the split name feature is not enabled. """
    #     res = super().fields_get(allfields, attributes)
    #     if 'appointment_resource_id' in res:
    #         res['appointment_resource_id']['ondelete'] = 'set null'
    #         res['appointment_resource_id']['required'] = False
    #     return res

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
            elif not line.appointment_resource_id.shareable or line.appointment_type_id.capacity_type == 'single_booking':
                line.capacity_used = line.appointment_resource_id.capacity
            else:
                line.capacity_used = 0 
