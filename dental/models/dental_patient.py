from odoo import api, models, fields, Command


class DentalPatient(models.Model):

    _name = "dental.patient"
    _description = "Dental Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    image = fields.Image('Image')
    state = fields.Selection(string='Status', default='new',
                             selection=[('new', 'New'), ('to_do_today', 'To Do Today'), ('done', 'Done'), ('to_invoice', 'To Invoice')])

    # Medical Field
    gp_id = fields.Many2one('res.partner', string="GP's Name")
    gp_phone = fields.Char(related='gp_id.phone',
                           string="GP's Phone", readonly=True)
    chronic_conditions_ids = fields.Many2many(
        'dental.chronic.conditions', string="Chronic Conditions")
    medication_ids = fields.Many2many('dental.medication', string="Medication")
    hospitalized_this_year = fields.Text(string="Hospitalised this Year")
    allergies_ids = fields.Many2many('dental.allergies', string="Allergies")
    notes = fields.Text(string='Notes')
    habits_substance_abuse_ids = fields.Many2many(
        'dental.habits', string="Habits/Substance Abuse")
    under_specialist_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric History")

    female = fields.Boolean(string="Female")
    is_pregnant = fields.Boolean(string="Are you pregnant?")
    is_nursing = fields.Boolean(string="Are you nursing?")
    hormone_treatment = fields.Selection([
        ('hormone_replacement_treatment', 'Hormone Replacement Treatment'),
        ('birth_control', 'Birth control'),
        ('neither', 'Neither')
    ], string="Are you on...?", default='neither')

    # Medical Aid
    medical_aid_id = fields.Many2one(
        'dental.medical.aids', string="Medical Aid")
    medical_aid_plan = fields.Char(string='Medical Aid Plan')
    medical_aid_number = fields.Integer(string='Medical Aid Number')
    main_member_code = fields.Integer(string='Medical Member Code')
    dependent_code = fields.Integer(string='Dependent Code')

    # Patient Details
    emergency_contact_id = fields.Many2one(
        'res.partner', string="Emergency Contact")
    mobile = fields.Char(related='emergency_contact_id.phone', string='Mobile')

    company_school_id = fields.Many2one(
        'res.partner', string="Company or School")
    occupation_grade = fields.Char(string="Occupation or Grade")
    identity_number = fields.Char(string="Identity Number")
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('female', 'Female'),
        ('male', 'Male'),
        ('neither', 'Neither')
    ], string="Gender")
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string="Marital Status")

    consent_signature = fields.Binary(string="Consent Signature")
    consent_date = fields.Date(string="Consent Date")

    # Gurantor Details
    guarantor_id = fields.Many2one(
        'res.users', string="Guarantor")
    guarantor_mobile = fields.Char(
        related='guarantor_id.mobile', string="Guarantor Mobile Phone", readonly=True)
    guarantor_phone = fields.Char(related='guarantor_id.phone', string="Phone")
    guarantor_email = fields.Char(related='guarantor_id.email', string="Email")

    tags = fields.Char(string="Tags")
    company_id = fields.Many2one(
        'res.company', string="Company")

    # History Details
    history_ids = fields.One2many('dental.medical.history', 'patient_id')

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == 'to_invoice':
            move_vals = {
                'partner_id': self.guarantor_id.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                "invoice_line_ids": [
                    Command.create({
                        "name": "consultant fees",
                        "quantity": 1,
                        "price_unit": 1000
                    }),
                ],

            }
            self.env['account.move'].create(move_vals)

    def action_book_appointment(self):
        self.state = 'to_invoice'
        vals = {
            'name': 'Dental Patient Appointnment ',
            'appointment_duration': 1,
            'appointment_tz': self.env.user.tz,
            'max_schedule_days': 15,
            'min_cancellation_hours': 45,
            'min_schedule_hours': 30,
            'schedule_based_on': 'users'

        }
        self.env['appointment.type'].create(vals)
