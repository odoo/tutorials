from odoo import fields, models


class CalendarBookingLine(models.Model):
    _inherit = 'calendar.booking.line'
    _description = "Meeting User/Resource Booking"

    appointment_resource_id = fields.Many2one('appointment.resource', 'Resource', ondelete='cascade', required=False, readonly=True)
    appointment_user_id = fields.Many2one('res.users', 'Users', ondelete='cascade', readonly=True)
