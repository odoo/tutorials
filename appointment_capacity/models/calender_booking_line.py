from odoo import fields,models

class CalenderBookingLine(models.Model):
    _inherit = "calendar.booking.line"

    appointment_resource_id = fields.Many2one('appointment.resource', 'Resource', ondelete='cascade', required=False)
    appointment_user_id = fields.Many2one('res.users', string="Appointment User", ondelete="cascade")
