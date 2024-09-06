from odoo import models, fields, Command


class DentalPatients(models.Model):
    _name = "dental.patient"
    _description = "Patients"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('todotoday', 'To Do Today'),
        ('done', 'Done'),
        ('toinvoice', 'To Invoice')
    ], default='new', tracking=True)

    gp_id = fields.Many2one('res.partner', string="GP's Name")
    gp_phone = fields.Char(related='gp_id.phone', string="GP's Phone", readonly=True)
    chronic_conditions = fields.Many2many('chronic.conditions', string="Chronic Conditions")
    medication = fields.Many2many('dental.medication', string="Medication")
    hospitalized_this_year = fields.Boolean(string="Hospitalised this Year")
    allergies = fields.Many2many('dental.allergies', string="Allergies")
    habits_substance_abuse = fields.Many2many('habits.substance', string="Habits and Substance Abuse")
    under_specialist_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric History")
    image_1920 = fields.Image(string="Image")
    gender = fields.Selection([
        ('female', 'Female'),
        ('male', 'Male'),
        ('neither', 'Neither')
    ], string="Gender")
    is_pregnant = fields.Boolean(string="Are you pregnant?", default=False, help="Visible if gender is Female")
    is_nursing = fields.Boolean(string="Are you nursing?", default=False, help="Visible if gender is Female")
    hormone_treatment = fields.Selection([
        ('hormone', 'Hormone Replacement Treatment'),
        ('birth_control', 'Birth control'),
        ('neither', 'Neither')
    ], string="Are you on...", default='neither', help="Visible if gender is Female")

    medical_aid_id = fields.Many2one('medical.aids', string="Medical Aid")
    medical_aid_plan = fields.Char(string="Medical Aid Plan")
    medical_aid_number = fields.Char(string="Medical Aid Number")
    main_number_code = fields.Char(string="Main Number Code")
    dependant_code = fields.Char(string="Dependant Code")

    # Fields for Patient Details
    emergency_contact_id = fields.Many2one('res.partner', string="Emergency Contact")
    mobile = fields.Char(related='emergency_contact_id.phone', string="Mobile", readonly=True)
    company_id = fields.Many2one('res.company', string="Company/School")
    occupation = fields.Char(string="Occupation/Grade")
    identity_number = fields.Char(string="Identity Number")
    date_of_birth = fields.Date(string="Date of Birth")
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string="Marital Status")

    # Fields for Consent Form
    consent_signature = fields.Binary(string="Consent Signature")
    consent_date = fields.Date(string="Consent Date")

    guarantor_id = fields.Many2one('res.users', string="Guarantor")
    guarantor_mobile = fields.Char(related='guarantor_id.mobile', string="Guarantor Mobile Phone", readonly=False)
    guarantor_phone = fields.Char(related='guarantor_id.phone', string="Phone", readonly=True)
    guarantor_email = fields.Char(related='guarantor_id.email', string="Email", readonly=True)

    # Add this field to link history records
    patient_history_ids = fields.One2many('dental.patient.history', 'patient_id', string="Patient History")

    def action_invoice(self):
        self.state = 'toinvoice'
        move_vals = {
            'partner_id': self.guarantor_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": 100
                }),
            ],

        }
        self.env['account.move'].create(move_vals)

    def book_appointment_button(self):
        vals = {
            'name': f"{self.name}-Dentist Booking",
            'appointment_type_id': self.env.ref('appointment.appointment_type_dental_care').id,
            'duration': 0.5
        }
        self.env['calendar.event'].create(vals)
        self.state = 'toinvoice'
