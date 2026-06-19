from datetime import date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HealthAppointment(models.Model):
    _name = 'health.appointment'
    _description = "Manage Appointments"

    patient_id = fields.Many2one('health.patient')
    doctor_id = fields.Many2one('res.users', default=lambda r: r.env.user)
    appointment_date = fields.Date(default=lambda r: fields.Date.context_today(r),
                                   required=True)
    state = fields.Selection(
        selection=[
            ('scheduled', "Scheduled"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
        default='scheduled'
    )
    priority = fields.Selection(
        selection=[
            ('0', "Normal"),
            ('1', "High"),
            ('2', "Critical")
        ]
    )
    notes = fields.Text()
    patient_age = fields.Integer(related='patient_id.age')
    reschedule_count = fields.Integer(default=0)
    original_date = fields.Date()

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for rec in self:
            if rec.appointment_date < fields.Date.today() and rec.state == 'scheduled':
                raise ValidationError('(id:%d) Appointment Date cannot be in past' % rec.id)

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        weekday = self.appointment_date.weekday()
        if weekday in [5, 6]:
            raise UserError("Appointment cannot be in Weekends")

    @api.constrains('doctor_id', 'appointment_date')
    def _check_max_appointment(self):
        for rec in self:
            doctor_appointments = rec.search_count([
                ('doctor_id', '=', rec.doctor_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('id', '!=', rec.id),
            ])
            if doctor_appointments >= 5:
                raise ValidationError('Doctor is fully Booked today')

    @api.constrains('reschedule_count')
    def _check_rechedule(self):
        if self.reschedule_count > 3:
            raise ValidationError("Cannot Reschedule More than 3 times")

    @api.onchange('priority', 'patient_id')
    def _onchange_priority(self):
        if self.priority == '2' and self.patient_id.is_minor:
            senior_doctor = self.env['res.users'].browse(6)
            self.doctor_id = senior_doctor

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            same_day_appointments = self.search([
                ('appointment_date', '=', vals.get('appointment_date')),
                ('patient_id', '=', vals.get('patient_id'))
            ])
            critical_appointments = self.search_count([
                ('patient_id', '=', vals.get('patient_id')),
                ('priority', '=', '2'),
                ('state', '=', 'scheduled')
            ])

        if same_day_appointments:
            raise ValidationError('Appointment already Exist for the same day!')

        if critical_appointments > 2:
            raise ValidationError('Cant create critical appointments more than 2')

        appointments = super().create(vals_list)
        for record in appointments:
            if record.patient_id.state == 'draft':
                record.patient_id.state = 'confirmed'
        return appointments

    def action_reschedule(self):
        self.original_date = self.appointment_date
        self.appointment_date = fields.Date.context_today(self)
        self.reschedule_count += 1
        return True
