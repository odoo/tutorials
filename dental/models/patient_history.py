from odoo import fields, models
from datetime import date


class DentalPatientHistory(models.Model):
    _name = "patient.history"
    _description = "This model is for Patient History"

    name = fields.Char(required=True)
    date = fields.Date(default=date.today())
    description = fields.Char()
    tags = fields.Char()
    attend = fields.Boolean(string="Did not attend")
    responsible = fields.Char()
    patient_id = fields.Many2one("dental.patient", readonly=True)
    company = fields.Char()
    main_complaint = fields.Text()
    history = fields.Text()
    x_ray1 = fields.Binary(string="X-ray file 1")
    x_ray2 = fields.Binary(string="X-ray file 2")
    alligner_file1 = fields.Binary()
    alligner_file2 = fields.Binary()
    habits = fields.Text()
    extra_oral_observation = fields.Text()
    treatment_notes = fields.Text()
    call_out = fields.Boolean()
    scale_and_polish = fields.Boolean()
    flouride = fields.Boolean()
    filling_description = fields.Text()
    alligner = fields.Boolean(String="Alligner delivery and attachment placed")
    whitening = fields.Boolean()
    fissure_seallant_quality = fields.Float(string="Fissure Sealant-Quality")
    attachment_removed = fields.Boolean()
    alligner_scan = fields.Boolean(string="Alligner Follow-up Scan")
    other = fields.Text()
    notes = fields.Text()
    consulatation_type = fields.Selection(
        copy=False,
        selection=[
            ("full_consulatation", "Full Consultation with bite-wings and scan"),
            ("basic_consultation", "Basic Consulatation"),
            ("no_consulatation", "No Consulatation"),
        ],
    )
    tooth18_staining = fields.Boolean(string="18 Staining")
    tooth17_staining = fields.Boolean(string="17 Staining")
    tooth16_staining = fields.Boolean(string="16 Staining")
    tooth15_staining = fields.Boolean(string="15 Staining")
    tooth14_staining = fields.Boolean(string="14 Staining")
    tooth13_staining = fields.Boolean(string="13 Staining")
    tooth12_staining = fields.Boolean(string="12 Staining")
    tooth11_staining = fields.Boolean(string="11 Staining")
    tooth28_staining = fields.Boolean(string="28 Staining")
    tooth27_staining = fields.Boolean(string="27 Staining")
    tooth26_staining = fields.Boolean(string="26 Staining")
    tooth25_staining = fields.Boolean(string="25 Staining")
    tooth24_staining = fields.Boolean(string="24 Staining")
    tooth23_staining = fields.Boolean(string="23 Staining")
    tooth22_staining = fields.Boolean(string="22 Staining")
    tooth21_staining = fields.Boolean(string="21 Staining")
    tooth48_staining = fields.Boolean(string="48 Staining")
    tooth47_staining = fields.Boolean(string="47 Staining")
    tooth46_staining = fields.Boolean(string="46 Staining")
    tooth45_staining = fields.Boolean(string="45 Staining")
    tooth44_staining = fields.Boolean(string="44 Staining")
    tooth43_staining = fields.Boolean(string="43 Staining")
    tooth42_staining = fields.Boolean(string="42 Staining")
    tooth41_staining = fields.Boolean(string="41 Staining")
    tooth38_staining = fields.Boolean(string="38 Staining")
    tooth37_staining = fields.Boolean(string="37 Staining")
    tooth36_staining = fields.Boolean(string="36 Staining")
    tooth35_staining = fields.Boolean(string="35 Staining")
    tooth34_staining = fields.Boolean(string="34 Staining")
    tooth33_staining = fields.Boolean(string="33 Staining")
    tooth32_staining = fields.Boolean(string="32 Staining")
    tooth31_staining = fields.Boolean(string="31 Staining")
