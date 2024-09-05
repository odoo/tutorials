from odoo import fields, models


class DentalPatientHistory(models.Model):
    _name = "dental.patient.history"
    _description = "Table contains patient allergies details."

    name = fields.Char()
    patient = fields.Char()
    date = fields.Date(default=fields.Date.today())
    attend = fields.Boolean(string="Did not attend")
    responsible = fields.Char()
    tags = fields.Char()
    company = fields.Char()
    main_complaint = fields.Text()
    history = fields.Text()
    x_ray_file1 = fields.Binary()
    x_ray_file2 = fields.Binary()
    clear_alligner_file1 = fields.Binary()
    clear_alligner_file2 = fields.Binary()
    habits = fields.Text()
    extra_oral_observation = fields.Text()
    treatment_notes = fields.Text()
    consulatation_type = fields.Selection(
        copy=False,
        selection=[
            ("full consulatation", "Full Consultation with bite-wings and scan"),
            ("basic consultation", "Basic Consulatation"),
            ("no consulatation", "No Consulatation"),
        ])
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
    patient_id = fields.Many2one("dental.patients")
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


   