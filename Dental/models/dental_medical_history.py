from odoo import models, fields,api
from datetime import date

class DentalMedicalHistory(models.Model):
    _name = 'dental.medical.history'
    _description = 'Dental Medical History'

    history_id = fields.Many2one('dental.patient', string="History")
    name = fields.Char(string="Name", store=True)
    patient_id = fields.Many2one('dental.patient', string="Patient", required=True)
    responsible_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    date = fields.Date(string="Date", default=date.today())
    description = fields.Text(string="Description")
    did_not_attend = fields.Boolean(string="Did not attend", required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    main_complaint = fields.Text(string="Main Complaint")
    teeth_history = fields.Text(string="History")
    habits = fields.Text(string="Habits")
    extra_oral_observation = fields.Text(string="Extra-Oral Observation")
    xray_file_1 = fields.Image(string="X-ray file 1")
    xray_file_2 = fields.Image(string="X-ray file 2")
    clear_align_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_align_file_2 = fields.Binary(string="Clear Aligner File 2")
    
    
    # Billing Fileds
    consultation_type = fields.Selection([
        ('full', 'Full consultation with bite-wings and scan'),
        ('basic', 'Basic consultation'),
        ('none', 'No consultation')
    ], string="Consultation Type")

    call_out = fields.Boolean(string="Call Out")
    scale_and_polish = fields.Boolean(string="Scale and Polish")
    fluoride = fields.Boolean(string="Fluoride")
    filling_description = fields.Text(string="Filling Description")

    aligner_delivery = fields.Boolean(string="Aligner delivery and attachment placed")
    whitening = fields.Boolean(string="Whitening")
    fissure_sealant_qty = fields.Float(string="Fissure Sealant - Quantity", digits=(6, 2))

    attachments_removed = fields.Boolean(string="Attachments Removed")
    aligner_follow_up_scan = fields.Boolean(string="Aligner Follow-up Scan")

    other_description = fields.Text(string="Other")
    notes = fields.Text(string="Notes")

    @api.depends('patient_id', 'date')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.patient_id.name} - {record.date}" if record.patient_id and record.date else "New History"
