from odoo import fields, models


class HistoryModel(models.Model):
    _name = "pateint.history"
    _description = "History"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    display_name = fields.Char()
    description = fields.Text()
    tags = fields.Char(string="Tags")
    patient_id = fields.Many2one("dental.patients")
    did_not_attend = fields.Boolean(string="Did Not Attend")
    responsible = fields.Char("Responsile")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    history = fields.Text(string="History")
    habits = fields.Text(string="Habits")
    extra_oral_observation = fields.Text(string="Extra-Oral Observation")
    xray_file_1 = fields.Image(string="X-ray File 1")
    xray_file_2 = fields.Image(string="X-ray File 2")
    clear_aligner_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_aligner_file_1_name = fields.Char(string="Clear Aligner File 1 Name")
    clear_aligner_file_2 = fields.Binary(string="Clear Aligner File 2")
    clear_aligner_file_2_name = fields.Char(string="Clear Aligner File 2 Name")
    consultation_type = fields.Selection(
        [
            ("full_consultation", "Full Consultation with Bite-Wings and Scan"),
            ("basic_consultation", "Basic Consultation"),
            ("no_consultation", "No Consultation"),
        ],
        string="Consultation Type",
    )

    call_out = fields.Boolean(string="Call Out")
    scale_polish = fields.Boolean(string="Scale and Polish")
    flouride = fields.Boolean(string="Flouride")
    aligner_delivery_attachment = fields.Boolean(
        string="Aligner Delivery and Attachment Placed"
    )
    whitening = fields.Boolean(string="Whitening")
    attachments_removed = fields.Boolean(string="Attachments Removed")
    aligner_followup_scan = fields.Boolean(string="Aligner Follow-up Scan")
    filling_description = fields.Text(string="Filling Description")
    other_notes = fields.Text(string="Other")
    fissure_sealant_qty = fields.Float(
        string="Fissure Sealant - Quantity", digits=(6, 2)
    )
    additional_notes = fields.Text(string="Additional Notes")
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
