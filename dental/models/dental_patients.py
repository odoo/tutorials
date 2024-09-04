import base64
from odoo import api, fields, models
from odoo.tools.misc import file_open


class Patients(models.Model):
    _name = "dental.patients"
    _description = "Detail Patients records"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Name", required=True)
    patient_image = fields.Image("Patient Image")
    hospitalised = fields.Char("Hospitalised this year")
    under_specialist_care = fields.Char()
    psychiatric_history = fields.Char()
    chronic_condition = fields.Many2many("dental.chronic.condition")
    medication = fields.Many2many("dental.medication")
    habits = fields.Many2many("dental.habits.abuse", string="Haits/Substance Abuse")
    allergy_ids = fields.Many2many("dental.allergies", string="Allergies")
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("today", "To do today"),
            ("done", "Done"),
            ("invoice", "To invoice"),
        ],
    )
    female = fields.Boolean(string="FEMALE")
    pregnant = fields.Boolean(string="Are you pregnant")
    nursing = fields.Boolean(string="Are you nursing")
    neither = fields.Selection(
        copy=False,
        default="neither",
        selection=[
            ("neither", "Neither"),
            ("Hormone", "Hormone Replacement Treatment"),
            ("female", "Birth Control"),
        ],
        string="Are you on...",
    )
    medical_aid_plan = fields.Char()
    main_member_code = fields.Integer()
    dependent_code = fields.Char()
    ocupation_grade = fields.Char()
    identity_no = fields.Char()
    birth_data = fields.Date()
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("transgender", "Transgender"),
        ],
    )
    marital_status = fields.Selection(
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorsed", "Divorsed"),
            ("widowed", "Widowed"),
        ]
    )
    note = fields.Text()
    gp_name = fields.Many2one("res.users", string="GP's Name")
    history_ids = fields.One2many("dental.history", "patient")
