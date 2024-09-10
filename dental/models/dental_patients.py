from odoo import models, fields, Command, api


class DentalPatients(models.Model):
    _name = "dental.patient"
    _description = "patients"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    stage = fields.Selection(
        string='Stage',
        selection=[('new', 'New'), ('to do today', 'To Do Today'), ('done', 'Done'), ('to invoice', 'To Invoice')],
        help='stage of the appointment',
        required=True,
        default='new')
    doctor_id = fields.Many2one(
        'res.partner',
        string="GP's Name",
        copy=False,
        help="The Genereal practioner for this patient")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        copy=False
    )
    guarantor_id = fields.Many2one(
        'res.users',
        string="Guarantor",
        copy=False
    )
    guarantor_phone = fields.Char(string="Guarantor Mobile Phone", related="guarantor_id.phone")
    phone = fields.Char(string="Phone")
    guarantor_email = fields.Char(string="Email", related="guarantor_id.email")
    guarantor_company = fields.Many2one('res.company')
    tag_ids = fields.Many2many('dental.tags', string="Tags")

    image = fields.Image()
    doc_phone_number = fields.Char(string="GP's Phone", related="doctor_id.phone")
    chronic_conditions_ids = fields.Many2many('chronic.conditions', string="Chronic Condtions")
    allergies_ids = fields.Many2many('dental.allergies', string="Allergies")
    habits_substance_ids = fields.Many2many('habits.substance', string="Habits and substance abuse")
    medication_ids = fields.Many2many('dental.medication', string="Medication")
    hospitalized = fields.Char(string="Hospitalized this year")
    specialized_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric history")
    gender = fields.Selection(
        string="Gender",
        selection=[('female', 'Female'), ('male', 'Male'), ('neither', 'Neither')],
        required=True,
        default='neither')
    pregnant = fields.Boolean(string="Are you pregnant?", required=True, default=False)
    nursing = fields.Boolean(string="Are you nursing?", required=True, default=False)
    hormone = fields.Selection(
        string="Are you on hormone therapy?",
        selection=[('hrt', 'Hormone Replacement Treatment'), ('birth control', 'Birth Conrol'), ('neither', 'Neither')],
        required=True,
        default='neither')
    occupation = fields.Char(string="Occupation")
    identity_num = fields.Char(string="Identity number")
    birthdate = fields.Date(string="Date of birth", required=True)
    maritial_status = fields.Selection(
        string="Maritial Status",
        selection=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')],
        required=True,
        default='single')
    emergency_contact_id = fields.Many2one(
        'res.users',
        string="Emergency Contact",
        copy=False
    )
    emergency_contact_phone = fields.Char(string="Mobile", related="emergency_contact_id.phone")
    consent_date = fields.Date(string="Consent Date")
    consent_signature = fields.Binary(string="Consent Signature")
    notes = fields.Text()
    insurance_id = fields.Many2one('medical.aids')
    medical_aids_plan = fields.Char(string="Medical Aid Plan")
    medical_aids_number = fields.Char(string="Medical Aid Number")
    main_member_code = fields.Char(string="Main Member Code")
    depedent_code = fields.Char(string="Dependent Code")
    medical_history_ids = fields.One2many('medical.history', 'patient_id', string="Medical History")

    @api.onchange("stage")
    def _onchange_stage(self):
        if self.stage == 'to invoice':
            self.guarantor_id = self.env.user.id
            move_vals = {
            'partner_id': self.guarantor_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                "name": "consultation fees",
                "quantity": 1,
                "price_unit": 500
            })
            ]
            }
            self.env['account.move'].create(move_vals)

    def book_invoice_button(self):
        self.stage = 'to invoice'
        self.guarantor_id = self.env.user.id
        move_vals = {
            'partner_id': self.guarantor_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                "name": "consultation fees",
                "quantity": 1,
                "price_unit": 500
            })
            ]
        }
        self.env['account.move'].create(move_vals)

    def book_appointment_button(self):
        move_vals = {
            'duration': 1,
            'appointment_type_id': self.env.ref('appointment.appointment_type_dental_care').id,
            'name': f"{self.name}-Dentist Appointment"
        }
        self.env['calendar.event'].create(move_vals)
