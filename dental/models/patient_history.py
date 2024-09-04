from odoo import fields, models, api
from datetime import date


class PatientHistory(models.Model):
    _name = "patient.history"
    _description = "Patient History"

    history_id = fields.Many2one('dental.patient', string="History")
    name = fields.Char(string="Name", compute="_compute_name", store=True)
    patient_id = fields.Many2one('dental.patient', string="Patient", required=True)
    responsible_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    date = fields.Date(string="Date", default=date.today())
    description = fields.Text(string="Description")
    did_not_attend = fields.Boolean(string="Did not attend")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    main_complaint = fields.Text(string="Main Complaint")
    teeth_history = fields.Text(string="History")
    habits = fields.Text(string="Habits")
    extra_oral_observation = fields.Text(string="Extra-Oral Observation")
    xray_file_1 = fields.Binary(string="X-ray file 1")
    xray_file_2 = fields.Binary(string="X-ray file 2")
    clear_align_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_align_file_2 = fields.Binary(string="Clear Aligner File 2")
    teeth_chart = fields.Char(string="Teeth Chart")
    treatment_notes = fields.Text(string="Treatment Notes")
    tags = fields.Char(string="Tags")

    consultation_type = fields.Selection([
        ('full_consultation', 'Full Consultation with Bitewings and Scan'),
        ('basic_consultation', 'Basic Consultation'),
        ('no_consultation', 'No Consultation')
    ], string="Consultation Type")

    call_out = fields.Boolean(string="Call Out")
    scale_and_polish = fields.Boolean(string="Scale and Polish")
    fluoride = fields.Boolean(string="Fluoride")
    filling_description = fields.Text(string="Filling Description")

    aligner_delivery = fields.Boolean(string="Aligner Delivery and Attachment Placed")
    whitening = fields.Boolean(string="Whitening")

    fissure_sealant_qty = fields.Float(
        string="Fissure Sealant Quantity", digits=(6, 2))

    attachments_removed = fields.Boolean(string="Attachments Removed")
    aligner_followup_scan = fields.Boolean(string="Aligner Follow-up Scan")

    other_notes = fields.Text(string="Other Notes")

    upper_18 = fields.Boolean(string="18 Staining")
    upper_17 = fields.Boolean(string="17 Staining")
    upper_16 = fields.Boolean(string="16 Staining")
    upper_15 = fields.Boolean(string="15 Staining")
    upper_14 = fields.Boolean(string="14 Staining")
    upper_13 = fields.Boolean(string="13 Staining")
    upper_12 = fields.Boolean(string="12 Staining")
    upper_11 = fields.Boolean(string="11 Staining")
    upper_28 = fields.Boolean(string="28 Staining")
    upper_27 = fields.Boolean(string="27 Staining")
    upper_26 = fields.Boolean(string="26 Staining")
    upper_25 = fields.Boolean(string="25 Staining")
    upper_24 = fields.Boolean(string="24 Staining")
    upper_23 = fields.Boolean(string="23 Staining")
    upper_22 = fields.Boolean(string="22 Staining")
    upper_21 = fields.Boolean(string="21 Staining")

    lower_38 = fields.Boolean(string="38 Staining")
    lower_37 = fields.Boolean(string="37 Staining")
    lower_36 = fields.Boolean(string="36 Staining")
    lower_35 = fields.Boolean(string="35 Staining")
    lower_34 = fields.Boolean(string="34 Staining")
    lower_33 = fields.Boolean(string="33 Staining")
    lower_32 = fields.Boolean(string="32 Staining")
    lower_31 = fields.Boolean(string="31 Staining")
    lower_41 = fields.Boolean(string="41 Staining")
    lower_42 = fields.Boolean(string="42 Staining")
    lower_43 = fields.Boolean(string="43 Staining")
    lower_44 = fields.Boolean(string="44 Staining")
    lower_45 = fields.Boolean(string="45 Staining")
    lower_46 = fields.Boolean(string="46 Staining")
    lower_47 = fields.Boolean(string="47 Staining")
    lower_48 = fields.Boolean(string="48 Staining")

    @api.depends('patient_id', 'date')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.patient_id.name}-{record.date}" if record.patient_id and record.date else "New History"
