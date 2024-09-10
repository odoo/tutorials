from datetime import date
import logging
from odoo import Command, fields, models


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
         tracking=True,
    )
    female = fields.Boolean(string="FEMALE")
    pregnant = fields.Boolean(string="Are you pregnant")
    nursing = fields.Boolean(string="Are you nursing")
    neither = fields.Selection(
        copy=False,
        default="neither",
        selection=[
            ("neither", "Neither"),
            ("hormone", "Hormone Replacement Treatment"),
            ("female", "Birth Control"),
        ],
        string="Are you on...",
    )
    medical_aid = fields.Many2one("dental.medical.aid")
    medical_aid_plan = fields.Char()
    medical_aid_number = fields.Char()
    main_member_code = fields.Integer()
    dependent_code = fields.Char()
    ocupation_grade = fields.Char(string="Ocupation or Grade")
    identity_no = fields.Char(string="Identity number")
    birth_data = fields.Date(strong="Date of Birth")
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
    emergency_contact = fields.Many2one("res.users")
    mobile = fields.Char(related="emergency_contact.partner_id.phone")
    company_id = fields.Many2one("res.company")
    signature = fields.Image("Consent Signature", help="Signature", copy=False)
    guaranator = fields.Many2one("res.users")
    guaranator_mobile = fields.Char(
        related="guaranator.partner_id.mobile", string="Guaranator Mobile Phone"
    )
    guaranator_phone = fields.Char(
        related="guaranator.partner_id.phone", string="Phone"
    )
    guaranator_email = fields.Char(
        related="guaranator.partner_id.email", string="Email"
    )
    tag_ids = fields.Many2many("dental.tags", string="Tags")
    guaranter_company = fields.Many2one("res.company", string="Company")

    def generate_invoice_from_patient(self):
        logging.info("Generating invoice...")
        if self.state == "done":
            for patient in self:
                invoice_obj = self.env["account.move"]
                invoice_vals = {
                    "partner_id": patient.guaranator.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": date.today(),
                    "state": "draft",
                    "ref": patient.name,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": patient.name,
                                "quantity": 1,
                                "price_unit": 1000 * 0.06,
                                "invoice_date": date.today(),
                            }
                        )
                    ],
                }
                invoice_obj.create(invoice_vals)
            self.state = "invoice"
