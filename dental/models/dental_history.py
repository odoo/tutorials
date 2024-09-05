import datetime
from odoo import fields, models


class History(models.Model):
    _name = "dental.history"
    _description = "History of patients"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    tags = fields.Many2many("dental.tags")
    patient = fields.Many2one("dental.patients")
    date = fields.Date(default=datetime.datetime.now())
    did_not_attend = fields.Boolean(required=True)
    responsible = fields.Char()
    company_id = fields.Many2one("res.company")
    main_complaint = fields.Text()
    history = fields.Text()
    xfiel1 = fields.Image(string="X-ray file 1")
    xfiel2 = fields.Image(string="X-ray file 2")
    habits = fields.Text()
    oral_observation = fields.Text(string="Extra-Oral observation")
    aligner_file1 = fields.Binary(string="Clear Aligner File 1")
    aligner_file2 = fields.Binary(string="Clear Aligner File 2")
    treatment_notes = fields.Text()
    consultation_type = fields.Selection(
        copy=False,
        selection=[
            ("bite_wing", "Bite-wings"),
            ("scan", "Scan"),
            ("consultation", "Consultation"),
            ("no_consultation", "No Consultation"),
        ],
    )
    call_out = fields.Boolean()
    scale_polish = fields.Boolean(string="Scale and polish")
    flouride = fields.Boolean(string="Flouride")
    filling_description = fields.Text()
    aligner_delivery_place = fields.Boolean(
        string="Aligner delivery and attachmentplaced"
    )
    whitening = fields.Boolean()
    fissure_sealant_quantity = fields.Float()
    attachments_removed = fields.Boolean()
    aligner_follow = fields.Boolean(string="Aligner Follow-up Scan")
    other = fields.Text()
    notes = fields.Text()
    tooth_18_staining = fields.Boolean(string="18 Staining")
    tooth_17_staining = fields.Boolean(string="17 Staining")
    tooth_16_staining = fields.Boolean(string="16 Staining")
    tooth_15_staining = fields.Boolean(string="15 Staining")
    tooth_14_staining = fields.Boolean(string="14 Staining")
    tooth_13_staining = fields.Boolean(string="13 Staining")
    tooth_12_staining = fields.Boolean(string="12 Staining")
    tooth_11_staining = fields.Boolean(string="11 Staining")
    tooth_28_staining = fields.Boolean(string="28 Staining")
    tooth_27_staining = fields.Boolean(string="27 Staining")
    tooth_26_staining = fields.Boolean(string="26 Staining")
    tooth_25_staining = fields.Boolean(string="25 Staining")
    tooth_24_staining = fields.Boolean(string="24 Staining")
    tooth_23_staining = fields.Boolean(string="23 Staining")
    tooth_22_staining = fields.Boolean(string="22 Staining")
    tooth_21_staining = fields.Boolean(string="21 Staining")
    tooth_38_staining = fields.Boolean(string="38 Staining")
    tooth_37_staining = fields.Boolean(string="37 Staining")
    tooth_36_staining = fields.Boolean(string="36 Staining")
    tooth_35_staining = fields.Boolean(string="35 Staining")
    tooth_34_staining = fields.Boolean(string="34 Staining")
    tooth_33_staining = fields.Boolean(string="33 Staining")
    tooth_32_staining = fields.Boolean(string="32 Staining")
    tooth_31_staining = fields.Boolean(string="31 Staining")
    tooth_41_staining = fields.Boolean(string="41 Staining")
    tooth_42_staining = fields.Boolean(string="42 Staining")
    tooth_43_staining = fields.Boolean(string="43 Staining")
    tooth_44_staining = fields.Boolean(string="44 Staining")
    tooth_45_staining = fields.Boolean(string="45 Staining")
    tooth_46_staining = fields.Boolean(string="46 Staining")
    tooth_47_staining = fields.Boolean(string="47 Staining")
    tooth_48_staining = fields.Boolean(string="48 Staining")
