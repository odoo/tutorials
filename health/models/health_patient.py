from odoo import api, fields, models

class HealthPatient(models.Model):
    _name = 'health.patient'
    _description = "Patient model"

    _check_age = models.Constraint(
        'CHECK (age >= 0)',
        'Age must be greater than 0'
    )

    name = fields.Char(required=True)
    age = fields.Integer(default=0)
    gender = fields.Selection(
        selection=[
            ('male', "Male"),
            ('female', "Female")
        ]
    )
    is_minor = fields.Boolean()
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('confirmed', "Confirmed"),
            ('discharged', "Discharged")
        ],
        default='draft'
    )
    appointment_ids = fields.One2many('health.appointment', 'patient_id')
    appointment_count = fields.Integer(compute="_compute_appointment_count")
    visit_count = fields.Integer(compute='_compute_visit_stats')
    last_visit_date = fields.Date(compute='_compute_visit_stats')
    is_frequent_visitor = fields.Boolean(compute='_compute_visit_stats')
    discharge_notes = fields.Text()
    rating = fields.Integer(default=1)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    @api.depends('appointment_ids')
    def _compute_visit_stats(self):
        for rec in self:
            dates = rec.appointment_ids.filtered(lambda r: r.state == 'done')
            rec.visit_count = len(dates)
            rec.last_visit_date = max(dates.mapped("appointment_date"), default=False)
            rec.is_frequent_visitor = rec.visit_count > 5

    @api.onchange('age')
    def _onchange_age(self):
        self.is_minor = True if (self.age < 18) else False

    def action_confirm(self):
        self.state = 'confirmed'

    def action_discharge(self):
        self.state = 'discharged'
        doctors = self.appointment_ids.mapped('doctor_id.name')
        visited_dates = self.appointment_ids.filtered(lambda r: r.state == 'done').mapped('appointment_date')
        formatted_dates = ', '.join(d.strftime('%d-%m-%Y') for d in visited_dates)
        self.discharge_notes = f"Treated By: {', '.join(doctors)}\nTotal Visits: {self.visit_count}\nVisited dates: {formatted_dates}"
        self.appointment_ids.filtered(lambda r: r.state == 'scheduled').write({
            'state': 'cancelled'
        })
        return True

    def action_esclate_all(self):
        normal_appointments = self.appointment_ids.filtered(lambda r: r.priority == '0').write({
            'priority': '1'
        })
