from datetime import date
from odoo import fields, models


class History(models.Model):
    _name = "dental.history"
    _description = "History of patients"
    date = fields.Date(default=date.today())
    description = fields.Text()
    tags = fields.Char()
    dispaly_name = fields.Char()
    patient = fields.Many2one("dental.patient")
    did_not_attend = fields.Boolean()
    responsible = fields.Char()
    company = fields.Many2one("res.company")
    x_ray1 = fields.Image()
    x_ray2 = fields.Image()
    history = fields.Text()
    habits = fields.Text()
    extra_oral_observation = fields.Text()
    clear_aligner1 = fields.Image()
    clear_aligner2 = fields.Image()
    treatment_notes = fields.Text()
    consulatation_type = fields.Selection(
        copy=False,
        selection=[
            ("full_consulatation", "Full Consultation with bite-wings and scan"),
            ("basic_consultation", "Basic Consulatation"),
            ("no_consulatation", "No Consulatation"),
        ],
    )
    call_out = fields.Boolean()
    scale_and_polish = fields.Boolean()
    flouride = fields.Boolean()
    filling_description = fields.Text()
    alligner_delivery = fields.Boolean(String="Alligner delivery and attachment placed")
    whitening = fields.Boolean()
    fissure_seallant_quality = fields.Float(string="Fissure Sealant-Quality")
    attachment_removed = fields.Boolean()
    alligner_followup_scan = fields.Boolean(string="Alligner Follow-up Scan")
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
    teeth_11 = fields.Boolean(string="11 Staining")

    teeth_12 = fields.Boolean(string="12 Staining")
    teeth_13 = fields.Boolean(string="13 Staining")
    teeth_14 = fields.Boolean(string="14 Staining")
    teeth_15 = fields.Boolean(string="15 Staining")
    teeth_16 = fields.Boolean(string="16 Staining")
    teeth_17 = fields.Boolean(string="17 Staining")
    teeth_18 = fields.Boolean(string="18 Staining")
    teeth_19 = fields.Boolean(string="19 Staining")
    teeth_20 = fields.Boolean(string="20 Staining")
    teeth_21 = fields.Boolean(string="21 Staining")
    teeth_22 = fields.Boolean(string="22 Staining")
    teeth_23 = fields.Boolean(string="23 Staining")
    teeth_24 = fields.Boolean(string="24 Staining")
    teeth_25 = fields.Boolean(string="25 Staining")
    teeth_26 = fields.Boolean(string="26 Staining")
    teeth_27 = fields.Boolean(string="27 Staining")
    teeth_28 = fields.Boolean(string="28 Staining")
    teeth_31 = fields.Boolean(string="31 Staining")
    teeth_32 = fields.Boolean(string="32 Staining")
    teeth_33 = fields.Boolean(string="33 Staining")
    teeth_34 = fields.Boolean(string="34 Staining")
    teeth_35 = fields.Boolean(string="35 Staining")
    teeth_36 = fields.Boolean(string="36 Staining")
    teeth_37 = fields.Boolean(string="37 Staining")
    teeth_38 = fields.Boolean(string="38 Staining")
    teeth_39 = fields.Boolean(string="39 Staining")
    teeth_40 = fields.Boolean(string="40 Staining")
    teeth_41 = fields.Boolean(string="41 Staining")
    teeth_42 = fields.Boolean(string="42 Staining")
    teeth_43 = fields.Boolean(string="43 Staining")
    teeth_44 = fields.Boolean(string="44 Staining")
    teeth_45 = fields.Boolean(string="45 Staining")
    teeth_46 = fields.Boolean(string="46 Staining")
    teeth_47 = fields.Boolean(string="47 Staining")
    teeth_48 = fields.Boolean(string="48 Staining")
