from datetime import datetime, timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class DentalPatient(models.Model):
    _name = "dental.patient"
    _description = "This is patient Model for Dental"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    patient_image = fields.Image("Patient Image")
    chronic_ids = fields.Many2many("chronic.condition", string="Chronic Conditions")
    allergie_ids = fields.Many2many("allergies", string="Allergies")
    medication_ids = fields.Many2many("medication", "patient_id", string="Medication")
    habit_ids = fields.Many2many("habits", string="Habits / Substance Abuse")

    under_speciality = fields.Char(String="Under Specialist care")
    physicatric_history = fields.Char(string="Psychatric History")
    medicalaid_id = fields.Many2one("medical.aids", string="Medical Aid")
    medical_aid_plan = fields.Char(string="Medical Aid Plan")
    medical_aid_no = fields.Char(string="Medical Aid Number")
    main_member_code = fields.Integer(string="Main Memeber Code")
    dependent_code = fields.Char(string="Dependent Code")
    ocupation = fields.Char()
    identity_no = fields.Char()
    birth_date = fields.Date()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("todotoday", "To do today"),
            ("done", "Done"),
            ("toinvoice", "To invoice")
        ],
        default="new"
    )
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("transgender", "Transgender"),
        ],
    )
    isfemale = fields.Boolean()
    ispregnant = fields.Boolean()
    isnursing = fields.Boolean()
    areyouon = fields.Selection(
        selection=[
            ("hormonereplacetreatment", "Hormone Replacement Treatment "),
            ("female", "Birth Control"),
            ("neither", "Neither"),
        ],
    )
    description_female = fields.Char()
    hospitalised_year = fields.Char()
    marital_status = fields.Selection(
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorsed", "Divorsed"),
            ("widowed", "Widowed")    
        ]
    )
