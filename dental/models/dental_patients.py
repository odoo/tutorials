from odoo import fields, models


class DentalPatients(models.Model):
    _name = "dental.patients"
    _description = "Table contains dental patients details."
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char()
    patient_image = fields.Binary()
    state = fields.Selection(
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("to do today", "To do today"),
            ("done", "Done"),
            ("to invoice", "To invoice"),
        ],
        tracking=True,
    )
    chronic_condition_ids = fields.Many2many('dental.chronic.conditions')
    hospitalised = fields.Text(string="Hospitalised This Year")
    medication_ids = fields.Many2many('dental.medication')
    allergies_ids = fields.Many2many('dental.allergies')
    habits_ids = fields.Many2many('dental.habits')
    special_care = fields.Text(string="Under Specialist Care")
    psychiatric_history = fields.Text(string="Psychiatric History")
    pregnant = fields.Boolean(string="Are you pregnant?")
    nursing = fields.Boolean(string="Are you nursing?")
    hrt = fields.Selection(string="Are you on...",  selection=[
            ("hrt", "Hormone Replacement Treatment"),
            ("birth control", "Birth Control"),
            ("neither", "Neither"),])
    notes = fields.Text()
    medical_aid_id = fields.Many2one("dental.medical.aids")
    medical_aid_plan = fields.Char()
    medical_aid_number = fields.Integer()
    main_member_code = fields.Integer()
    dependant_code = fields.Integer()
    grade = fields.Text(string="Occupation or Grade")
    identity_number = fields.Char()
    date_of_birth = fields.Date()
    gender = fields.Selection(
        copy=False,
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("neither", "Neither"),
        ])
    marital_status = fields.Selection(
        copy=False,
        selection=[
            ("single", "Single"),
            ("marries", "Married"),
            ("divorced", "Divorced"),
        ])
    patient_history_id = fields.One2many("dental.patient.history","patient_id")
    gp_name_id = fields.Many2one('res.partner',string="GP's Name")
    gp_phone = fields.Char(
        string="GP's Phone", 
        related="gp_name_id.phone", 
        readonly=True
    )
    guarantor_id = fields.Many2one('res.partner', string='Guarantor')
    guarantor_phone = fields.Char(
        string='Guarantor Phone', 
        related='guarantor_id.phone', 
        readonly=True
    )
    guarantor_email = fields.Char(
        string='Guarantor Email', 
        related='guarantor_id.email', 
        readonly=True
    )
    guarantor_company = fields.Char(string="Company", related='guarantor_id.parent_id.name')
    guarantor_tags = fields.Many2many(string="Tags", related='guarantor_id.category_id')
    consent_signature = fields.Binary()
    consent_date = fields.Date()