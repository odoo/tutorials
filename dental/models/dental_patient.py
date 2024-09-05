from datetime import datetime, timedelta, date
from odoo import fields, models, api, Command
from odoo.exceptions import UserError, ValidationError


class DentalPatient(models.Model):
    _name = "dental.patient"
    _description = "This is patient Model for Dental"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    patient_image = fields.Image("Patient Image")
    gp_name = fields.Many2one("res.users")
    gp_phone = fields.Char(related="gp_name.partner_id.phone")
    history_ids = fields.One2many("patient.history", "patient_id")
    emegency_contact_id = fields.Many2one("res.users")
    mobile = fields.Char(related="emegency_contact_id.partner_id.phone")
    company_id = fields.Many2one("res.company")
    gurantor = fields.Many2one("res.users")
    gurantor_mobile = fields.Char(related="gurantor.partner_id.mobile")
    gurantor_company_id = fields.Many2one("res.company")
    gurantor_phone = fields.Char(related="gurantor.partner_id.phone")
    gurantor_tags = fields.Many2many(related="gurantor.partner_id.category_id")
    gurantor_email = fields.Char(related="gurantor.partner_id.email")
    consent_sign = fields.Image("Consent Sign")
    consent_date = fields.Date("Consent Date")
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
            ("toinvoice", "To invoice"),
        ],
        default="new",
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
    description_female = fields.Text()
    hospitalised_year = fields.Char()
    marital_status = fields.Selection(
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorsed", "Divorsed"),
            ("widowed", "Widowed"),
        ]
    )

    @api.onchange("state")
    def create_patient_invoice(self):
        if self.state == "toinvoice":
            for record in self:
                print(record.gurantor.id)
                values_property = {
                    "partner_id": record.gurantor.partner_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": date.today(),
                    "line_ids": [
                        Command.create(
                            {
                                "name": record.name,
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            }
                        ),
                    ],
                }
                self.env["account.move"].sudo().create(values_property)
