from odoo import models, fields, api
from datetime import date


class DentalPatientHistory(models.Model):
    _name = 'dental.patient.history'
    _description = 'Dental Patient History'

    # Basic information
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    patient_id = fields.Many2one('dental.patient', string="Patient", required=True)
    date = fields.Date(string="Date", default=fields.Date.context_today, required=True)
    main_complaint = fields.Text(string="Main Complaint")
    history = fields.Text(string="History")
    company_id = fields.Many2one('res.company', string='Company')
    did_not_attend = fields.Boolean(string="Did Not Attend")
    tags = fields.Char(string="Tags")

    # X-ray file uploads
    xray_file_1 = fields.Binary(string="X-ray File 1")
    xray_file_2 = fields.Binary(string="X-ray File 2")
    clear_aligner_file_1 = fields.Binary(string="Clear Aligner File 1")
    clear_aligner_file_2 = fields.Binary(string="Clear Aligner File 2")

    # Other details
    habits = fields.Text(string="Habits")
    extra_oral_observation = fields.Text(string="Extra-Oral Observation")

    # Tooth chart (for example purposes)
    teeth_chart = fields.Char(string="Teeth Chart")

    # Treatment notes
    treatment_notes = fields.Text(string="Treatment Notes")

    # Billing information
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

    # General notes field at the end
    notes = fields.Text(string="Additional Notes")

    @api.depends("patient_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.patient_id.name}-{date.today()}"

    def action_save_close(self):
        # Method to save and close the form view
        self.ensure_one()
        self.env['ir.actions.act_window'].browse(self._context.get('active_id')).write({'state': 'done'})
