from odoo import models, fields
from datetime import date


class DentalHistory(models.Model):
    _name = "dental.history"
    _description = "Dental history of patient"

    history_id = fields.Many2one("dental.patient")
    date = fields.Date(string="Date", default=date.today())
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    tags = fields.Char(string="Tags")
    patient = fields.Char()
    attend = fields.Boolean(string="Did not attend", required=True)
    responsible = fields.Char()
    company = fields.Many2one("res.company", string="Company")
    history = fields.Text(string="History")
    xray_file1 = fields.Binary(string="X-ray file 1")
    xray_file2 = fields.Binary(string="X-ray file 2")
    clear_aligner_file1 = fields.Binary(string="Clear Aligner File 1")
    clear_aligner_file2 = fields.Binary(string="Clear Aligner File 2")
    habits = fields.Text(string="Habits")
    extra_observation = fields.Text(string="Extra Oral Observation")
    treatment_notes = fields.Text(string="Treatment Notes")
    consulatation = fields.Selection(
        copy=False,
        selection=[
            (
                "full_consultation_and_scan",
                "Full Consultation with bite-wings and scan",
            ),
            ("basic_consultation", "Basic Consultation"),
            ("no_consultation", "No Consultation"),
        ],
        string="Consultation Type",
    )
    call_out = fields.Boolean(string="Call out")
    scale_and_polish = fields.Boolean(string="Scale and Push")
    flouride = fields.Boolean(string="Flouride")
    filling_description = fields.Text(string="Filling Description")
    aligner_attachment = fields.Boolean(
        string="Alligner delivery and attachment placed"
    )
    whitening = fields.Boolean(string="Whitening")
    fissure_sealant_quantity = fields.Float(string="Fissure Sealant-Quantity")
    remove_attachment = fields.Boolean(string="Attachment Removed")
    alligner_follow_up_scan = fields.Boolean(string="Alligner Follow-up Scan")
    other = fields.Text(string="Other")
    upper_18_staining = fields.Boolean(string="18 Staining")
    upper_17_staining = fields.Boolean(string="17 Staining")
    upper_16_staining = fields.Boolean(string="16 Staining")
    upper_15_staining = fields.Boolean(string="15 Staining")
    upper_14_staining = fields.Boolean(string="14 Staining")
    upper_13_staining = fields.Boolean(string="13 Staining")
    upper_12_staining = fields.Boolean(string="12 Staining")
    upper_11_staining = fields.Boolean(string="11 Staining")
    upper_28_staining = fields.Boolean(string="28 Staining")
    upper_27_staining = fields.Boolean(string="27 Staining")
    upper_26_staining = fields.Boolean(string="26 Staining")
    upper_25_staining = fields.Boolean(string="25 Staining")
    upper_24_staining = fields.Boolean(string="24 Staining")
    upper_23_staining = fields.Boolean(string="23 Staining")
    upper_22_staining = fields.Boolean(string="22 Staining")
    upper_21_staining = fields.Boolean(string="21 Staining")
    lower_31_staining = fields.Boolean(string="31 Staining")
    lower_32_staining = fields.Boolean(string="32 Staining")
    lower_33_staining = fields.Boolean(string="33 Staining")
    lower_34_staining = fields.Boolean(string="34 Staining")
    lower_35_staining = fields.Boolean(string="35 Staining")
    lower_36_staining = fields.Boolean(string="36 Staining")
    lower_37_staining = fields.Boolean(string="37 Staining")
    lower_38_staining = fields.Boolean(string="38 Staining")
    lower_41_staining = fields.Boolean(string="41 Staining")
    lower_42_staining = fields.Boolean(string="42 Staining")
    lower_43_staining = fields.Boolean(string="43 Staining")
    lower_44_staining = fields.Boolean(string="44 Staining")
    lower_45_staining = fields.Boolean(string="45 Staining")
    lower_46_staining = fields.Boolean(string="46 Staining")
    lower_47_staining = fields.Boolean(string="47 Staining")
    lower_48_staining = fields.Boolean(string="48 Staining")

    notes = fields.Text()
