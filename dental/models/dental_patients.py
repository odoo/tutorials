from odoo import models, fields, Command


class DentalPatients(models.Model):
    _name = "dental.patient"
    _description = "Patients"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    portal_access = fields.Boolean(string="Portal Access", default=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    state = fields.Selection([
        ('new', 'New'),
        ('todotoday', 'To Do Today'),
        ('done', 'Done'),
        ('toinvoice', 'To Invoice')
    ], default='new', tracking=True)
    image = fields.Image(string="Image")
    gp_id = fields.Many2one('res.partner', string="GP's Name")
    gp_phone = fields.Char(related='gp_id.phone', string="GP's Phone", readonly=True)
    chronic_conditions = fields.Many2many('chronic.conditions', string="Chronic Conditions")
    medication = fields.Many2many('dental.medication', string="Medication")
    hospitalized_this_year = fields.Boolean(string="Hospitalised this Year")
    allergies = fields.Many2many('dental.allergies', string="Allergies")
    habits_substance_abuse = fields.Many2many('habits.substance', string="Habits and Substance Abuse")
    under_specialist_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric History")
    is_pregnant = fields.Boolean(string="Are you pregnant?", default=False)
    is_nursing = fields.Boolean(string="Are you nursing?", default=False)
    hormone_treatment = fields.Selection([
        ('hormone', 'Hormone Replacement Treatment'),
        ('birth_control', 'Birth control'),
        ('neither', 'Neither')
    ], string="Are you on...?", default='neither')
    medical_aids = fields.Many2one('medical.aids', string="Medical Aids")
    medical_aids_plan = fields.Char(string="Medical Aids Plan")
    medical_aid_number = fields.Integer(string="Medical Aids Number")
    main_member_code = fields.Integer(string="Main Member Code")
    depandant_code = fields.Integer(string="Dependant Code")
    medical_aids_note = fields.Text(string="Medical Aids Notes")

    # Emergency Contact Section

    emergency_contact_id = fields.Many2one('res.partner', string="Emergency Contact")
    emergency_contact_mobile = fields.Char(related='emergency_contact_id.phone', string="Mobile", readonly=True)

    # Patient Details Section
    company_or_school_id = fields.Many2one('res.users', string="Company or School")
    occupation_or_grade = fields.Char(string="Occupation or Grade")
    identity_number = fields.Char(string="Identity Number")
    date_of_birth = fields.Date(string="Date of Birth")

    gender = fields.Selection([
        ('female', 'Female'),
        ('male', 'Male'),
        ('neither', 'Neither')
    ], string="Gender", default='female')

    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string="Marital Status", default='single')

    # Consent Form Section
    consent_signature = fields.Binary(string="Consent Signature")
    consent_date = fields.Date(string="Consent Date")

    guarantor_name = fields.Many2one('res.users', string="Guarantor Name")
    guarantor_mobile = fields.Char(related='guarantor_name.phone', string="Mobile", readonly=True)
    guarantor_email = fields.Char(related='guarantor_name.email', string="Email", readonly=True)
    guarantor_phone = fields.Char(string="Phone")
    tags = fields.Char(string="Tags")
    company_id = fields.Many2one('res.company', string="Company")

    history_ids = fields.One2many('patient.history', 'history_id', string="History")

    def action_toinvoice(self):
        self.state = 'toinvoice'
        move_vals = {
            'partner_id': self.guarantor_name.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            "invoice_line_ids": [
                Command.create({
                    "name": "consultant fees",
                    "quantity": 1,
                    "price_unit": 500
                }),
            ],

        }
        self.env['account.move'].create(move_vals)

    def book_appointment_button(self):
        move_vals = {
            'appointment_duration': 1,
            'appointment_tz': self.env.user.tz,
            'assign_method': 'resource_time',
            'max_schedule_days': 1,
            'min_cancellation_hours': 24,
            'min_schedule_hours': 48,
            'name': 'Appointment',
            'schedule_based_on': 'users',
        }
        self.env['appointment.type'].sudo().create(move_vals)
