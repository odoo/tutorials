import datetime
from odoo import fields, models


class History(models.Model):
    _name = "dental.history"
    _description = "History of patients"

    name = fields.Char()
    tags = fields.Many2many("dental.tags")
    patient = fields.Many2one("dental.patients")
    date = fields.Date(default=datetime.datetime.now())
    did_not_attend = fields.Boolean(required=True)
    responsible = fields.Char()
    company_id = fields.Many2one("res.company")
    main_complaint = fields.Text()
    history = fields.Text()
    xfiel1 = fields.Image(string="X-ray file 1")
    xfiel2 = fields.Image(string="X-ray file 2")
    habits = fields.Text()
    oral_observation = fields.Text(string="Extra-Oral observation")
    aligner_file1 = fields.Binary(string="Clear Aligner File 1")
    aligner_file2 = fields.Binary(string="Clear Aligner File 2")
    treatment_notes = fields.Text()
    consultation_type = fields.Selection(
        copy=False,
        selection=[
            ("bite_wing", "Bite-wings"),
            ("scan", "Scan"),
            ("consultation", "Consultation"),
            ("no_consultation", "No Consultation"),
        ],
    )
    call_out = fields.Boolean()
    scale_polish = fields.Boolean(string="Scale and polish")
    flouride = fields.Boolean(string="Flouride")
    filling_description = fields.Text()
    aligner_delivery_place = fields.Boolean(
        string="Aligner delivery and attachmentplaced"
    )
    whitening = fields.Boolean()
    fissure_sealant_quantity = fields.Float()
    attachments_removed = fields.Boolean()
    aligner_follow = fields.Boolean(string="Aligner Follow-up Scan")
    other = fields.Text()
    notes = fields.Text()
