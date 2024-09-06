from datetime import date
from odoo import Command, fields, models


class PatientModel(models.Model):
    _name = "dental.patients"
    _description = "Dental Patients"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("to do today", "To Do Today"),
            ("done", "Done"),
            ("to invoice", "To Invoice"),
        ],
        tracking=True,
        default="new",
    )
    image = fields.Image(string="Image")
    sequence = fields.Integer("Sequence")
    gp_name = fields.Many2one("res.partner", string="Gp's Name")
    gp_phone = fields.Char(string="Gp's Phone", related="gp_name.phone", store=True)
    chronic_ids = fields.Many2many("chronic.condition", string="Chronic Condition")
    aleergies_ids = fields.Many2many("symptoms.allergies", string="Allergies")
    habits_ids = fields.Many2many("symptoms.habits", string="Habits/Substance Abuse")
    medication = fields.Many2many("medication", string="Medication")
    hospitalised_this_year = fields.Text()
    under_special_care = fields.Text(string="Under Specialist Care")
    psychiatric_history = fields.Text(string="Psychiatric History")
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("neither", "Neither"),
        ],
    )
    are_you_pregnant = fields.Boolean(string="Are You Pregnant")
    are_you_nursing = fields.Boolean(string="Are You Nursing")
    are_you_on = fields.Selection(
        selection=[
            ("hormon replacement treatment", "Hormon Replacement Treatment"),
            ("birth control", "Birth Control"),
            ("neither", "Neither"),
        ],
    )
    notes = fields.Text()
    medical_aid_id = fields.Many2one("medical.aids", string="Medical Aid")
    medical_aid_plan = fields.Text(string="Medical Aid Plan")
    medical_aid_number = fields.Text(string="Medical Aid Number")
    main_member_code = fields.Text(string="Main Member Code")
    dependant_code = fields.Text(string="Dependant Code")
    occupation_or_grade = fields.Text(string="Occupation Or Grade")
    identity_number = fields.Text(string="Identity Number")
    date_of_birth = fields.Date(string="Date Of Birth")
    marital_status = fields.Selection(
        selection=[
            ("single", "single"),
            ("married", "married"),
            ("divorced", "divorced"),
            ("widowed", "widowed"),
        ],
        string="Marital Status",
    )
    phone_number = fields.Char(string="Mobile")
    history_id = fields.One2many("pateint.history", "patient_id", string="History")
    guarantor_id = fields.Many2one("res.partner", string="Guarantor")
    guarantor_phone = fields.Char(
        string="Guarantor Phone", related="guarantor_id.phone", readonly=True
    )
    guarantor_email = fields.Char(
        string="Guarantor Email", related="guarantor_id.email", readonly=True
    )
    guarantor_company = fields.Char(
        string="Company", related="guarantor_id.parent_id.name"
    )
    guarantor_tags = fields.Many2many(string="Tags", related="guarantor_id.category_id")

    def action_open_invoice(self):
        if self.state == "to invoice":
            for patient_id in self:
                self.ensure_one()
                invoice_obj = self.env["account.move"]
                invoice_vals = {
                    "partner_id": patient_id.guarantor_id.id,
                    "move_type": "out_invoice",
                    "invoice_date": date.today(),
                    "state": "draft",
                    "ref": patient_id.name,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": patient_id.name,
                                "quantity": 1,
                                "price_unit": 1000 * 0.06,
                                "invoice_date": date.today(),
                            }
                        )
                    ],
                }
                invoice_obj.create(invoice_vals)
