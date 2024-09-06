from datetime import date
from odoo import fields, models, Command


class patient(models.Model):
    _name = "dental.patient"
    _description = "dental patient"
    _order = "sequence, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    state = fields.Selection(
        default="new",
        selection=[
            ("new", "New"),
            ("today", "To do today"),
            ("done", "Done"),
            ("invoice", "To Invoice"),
        ],
        tracking=True,
    )
    sequence = fields.Integer("Sequence")
    patient_image = fields.Image("Image")
    under_speciality = fields.Char()
    physicatric_history = fields.Char()
    occupation = fields.Char()
    identity_no = fields.Char()
    birth_data = fields.Date()
    notes = fields.Text()
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("transgender", "Transgender"),
        ],
    )
    ispregnant = fields.Boolean(string="Are you pregnant")
    isnursing = fields.Boolean(string="Are you nursing")
    areyouon = fields.Selection(
        selection=[
            ("hormonereplacetreatment", "Hormone Replacement Treatment "),
            ("female", "Birth Control"),
            ("neither", "Neither"),
        ],
        string="Are you on...",
    )
    description_female = fields.Char()
    hospitalised_year = fields.Char(string="Hospitalised this year")
    marital_status = fields.Selection(
        selection=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorsed", "Divorsed"),
            ("widowed", "Widowed"),
        ]
    )
    chronic_ids = fields.Many2many(
        "dental.chronic.condition", string="Chronic Conditions"
    )
    allergies_ids = fields.Many2many("dental.allergies", string="Allergies")
    medication_ids = fields.Many2many("dental.medication", string="Medication")
    medical_aids_ids = fields.Many2one("dental.medical.aids", string="Medical Aid")
    habits_abuse_ids = fields.Many2many(
        "dental.habits.abuse", string="Habits/Substance Abuse"
    )
    history_ids = fields.One2many("dental.history", "patient")
    gpname = fields.Many2one(
        "res.users", string="GP's Name", copy=False, ondelete="cascade"
    )
    medical_aid_plan = fields.Char(string="Medical Aid Plan")
    medical_aid_no = fields.Char(string="Medical Aid Number")
    main_member_code = fields.Integer(string="Main Memeber Code")
    dependent_code = fields.Char(string="Dependent Code")
    signature = fields.Image("Consent Signature", help="Signature", copy=False)
    emergency_contact = fields.Many2one("res.users")
    company_id = fields.Many2one("res.company")
    mobile = fields.Char(related="emergency_contact.partner_id.phone")
    guarantor = fields.Many2one("res.users")
    guarantor_mobile = fields.Char(related="guarantor.partner_id.mobile")
    tags_ids = fields.Many2many(related="guarantor.partner_id.category_id")
    guarantor_company_id = fields.Many2one("res.company")
    guarantor_phone = fields.Char(related="guarantor.partner_id.phone")
    guarantor_email = fields.Char(related="guarantor.partner_id.email")

    def button_to_invoice(self):
        self.state = "invoice"
        for record in self:
            Hosopital_fee = 100
            invoice_vals = {
                "partner_id": record.guarantor.partner_id.id,
                "move_type": "out_invoice",
                "invoice_date": date.today(),
                "line_ids": [
                    Command.create(
                        {
                            "name": "Hosopital Fee",
                            "price_unit": Hosopital_fee,
                        }
                    ),
                ],
            }
            self.env["account.move"].sudo().create(invoice_vals)
