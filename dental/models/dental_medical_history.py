from odoo import models, fields, api
from datetime import date


class DentalMedicalHistory(models.Model):
    _name = 'dental.medical.history'
    _description = 'Dental Mdeical History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Consultation Name", compute="_compute_name")
    date = fields.Date(
        string="Date", default=fields.Date.context_today, required=True)
    patient_id = fields.Many2one(
        'dental.patient', string="Patient", required=True)
    main_complaint = fields.Text(string="Main Complaint")
    history = fields.Text(string="History")
    tags = fields.Char(string="Tags")
    company_id = fields.Many2one('res.company', string='Company')
    did_not_attend = fields.Boolean(required=True)

    xray_file_1 = fields.Binary(string="X-ray File 1")
    xray_file_2 = fields.Binary(string="X-ray File 2")
    clear_aligner_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_aligner_file_2 = fields.Binary(string="Clear Aligner File 2")

    habits = fields.Text(string="Habits")
    extra_oral_observation = fields.Text(string="Extra-Oral Observation")

    teeth_chart = fields.Char(string="Teeth Chart")

    treatment_notes = fields.Text(string="Treatment Notes")

    consultation_type = fields.Selection([
        ('full_consultation', 'Full Consultation with Bitewings and Scan'),
        ('basic_consultation', 'Basic Consultation'),
        ('no_consultation', 'No Consultation')
    ], string="Consultation Type")

    call_out = fields.Boolean(string="Call Out")
    scale_and_polish = fields.Boolean(string="Scale and Polish")
    fluoride = fields.Boolean(string="Fluoride")

    filling_description = fields.Text(string="Filling Description")

    aligner_delivery = fields.Boolean(
        string="Aligner Delivery and Attachment Placed")
    whitening = fields.Boolean(string="Whitening")

    fissure_sealant_qty = fields.Float(
        string="Fissure Sealant Quantity", digits=(6, 2))

    attachments_removed = fields.Boolean(string="Attachments Removed")
    aligner_followup_scan = fields.Boolean(string="Aligner Follow-up Scan")

    other_notes = fields.Text(string="Other Notes")

    notes = fields.Text(string="Additional Notes")

    @api.depends("patient_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.patient_id.name}-{date.today()}"

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
