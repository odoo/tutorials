from odoo import models, fields, api
from datetime import date


class DentalMedicalHistory(models.Model):
    _name = 'dental.medical.history'
    _description = 'Dental Mdeical History'

    name = fields.Char(string="Consultation Name", compute="_compute_name")
    date = fields.Date(
        string="Date", default=fields.Date.context_today, required=True)
    patient_id = fields.Many2one(
        'dental.patient', string="Patient", required=True)
    main_complaint = fields.Char(string="Main Complaint")
    history = fields.Char(string="History")
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)
    did_not_attend = fields.Boolean(required=True)
    xray_file_1 = fields.Binary(string="X-ray File 1")
    xray_file_2 = fields.Binary(string="X-ray File 2")
    clear_aligner_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_aligner_file_2 = fields.Binary(string="Clear Aligner File 2")
    habits = fields.Char(string="Habits")
    extra_oral_observation = fields.Char(string="Extra-Oral Observation")
    treatment_notes = fields.Char(string="Treatment Notes")
    consultation_type = fields.Selection([
        ('full_consultation', 'Full Consultation with Bitewings and Scan'),
        ('basic_consultation', 'Basic Consultation'),
        ('no_consultation', 'No Consultation')
    ], string="Consultation Type")

    call_out = fields.Boolean(string="Call Out")
    scale_and_polish = fields.Boolean(string="Scale and Polish")
    fluoride = fields.Boolean(string="Fluoride")
    filling_description = fields.Char(string="Filling Description")
    aligner_delivery = fields.Boolean(
        string="Aligner Delivery and Attachment Placed")
    whitening = fields.Boolean(string="Whitening")
    fissure_sealant_qty = fields.Float(
        string="Fissure Sealant Quantity", digits=(6, 2))
    attachments_removed = fields.Boolean(string="Attachments Removed")
    aligner_followup_scan = fields.Boolean(string="Aligner Follow-up Scan")
    other_notes = fields.Char(string="Other Notes")

    # General notes field at the end
    notes = fields.Char(string="Additional Notes")

    upper_18_staining = fields.Boolean(string='18 Staining')
    upper_17_staining = fields.Boolean(string='17 Staining')
    upper_16_staining = fields.Boolean(string='16 Staining')
    upper_15_staining = fields.Boolean(string='15 Staining')
    upper_14_staining = fields.Boolean(string='14 Staining')
    upper_13_staining = fields.Boolean(string='13 Staining')
    upper_12_staining = fields.Boolean(string='12 Staining')
    upper_11_staining = fields.Boolean(string='11 Staining')
    upper_28_staining = fields.Boolean(string='28 Staining')
    upper_27_staining = fields.Boolean(string='27 Staining')
    upper_26_staining = fields.Boolean(string='26 Staining')
    upper_25_staining = fields.Boolean(string='25 Staining')
    upper_24_staining = fields.Boolean(string='24 Staining')
    upper_23_staining = fields.Boolean(string='23 Staining')
    upper_22_staining = fields.Boolean(string='22 Staining')
    upper_21_staining = fields.Boolean(string='21 Staining')
    lower_31_staining = fields.Boolean(string='31 Staining')
    lower_32_staining = fields.Boolean(string='32 Staining')
    lower_33_staining = fields.Boolean(string='33 Staining')
    lower_34_staining = fields.Boolean(string='34 Staining')
    lower_35_staining = fields.Boolean(string='35 Staining')
    lower_36_staining = fields.Boolean(string='36 Staining')
    lower_37_staining = fields.Boolean(string='37 Staining')
    lower_38_staining = fields.Boolean(string='38 Staining')
    lower_41_staining = fields.Boolean(string='41 Staining')
    lower_42_staining = fields.Boolean(string='42 Staining')
    lower_43_staining = fields.Boolean(string='43 Staining')
    lower_44_staining = fields.Boolean(string='44 Staining')
    lower_45_staining = fields.Boolean(string='45 Staining')
    lower_46_staining = fields.Boolean(string='46 Staining')
    lower_47_staining = fields.Boolean(string='47 Staining')
    lower_48_staining = fields.Boolean(string='48 Staining')

    @api.depends("patient_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.patient_id.name}-{date.today()}"
