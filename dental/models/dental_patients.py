from odoo import models, fields


class DentalPatients(models.Model):
    _name = "dental.patient"
    _description = "Patients"

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('todotoday', 'To Do Today'),
        ('done', 'Done'),
        ('toinvoice', 'To Invoice')
    ], default='new')

    gp_id = fields.Many2one('res.partner', string="GP's Name")
    gp_phone = fields.Char(related='gp_id.phone', string="GP's Phone", readonly=True)
    chronic_conditions = fields.Many2many('dental.condition', string="Chronic Conditions")
    medication = fields.Many2many('dental.medication', string="Medication")
    hospitalized_this_year = fields.Boolean(string="Hospitalised this Year")
    allergies = fields.Char(string="Allergies")
    habits_substance_abuse = fields.Char(string="Habits/Substance Abuse")
    under_specialist_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric History")
    female = fields.Boolean(string="Female")
    is_pregnant = fields.Boolean(string="Are you pregnant?", default=False)
    is_nursing = fields.Boolean(string="Are you nursing?", default=False)
    hormone_treatment = fields.Selection([
        ('hormone', 'Hormone Replacement Treatment'),
        ('birth_control', 'Birth control'),
        ('neither', 'Neither')
    ], string="Are you on...?", default='neither')

    medical_aid_id = fields.Many2one('medical.aids', string="Medical Aid")
    medical_aid_plan = fields.Char(string="Medical Aid Plan")
    medical_aid_number = fields.Char(string="Medical Aid Number")
    main_number_code = fields.Char(string="Main Number Code")
    dependant_code = fields.Char(string="Dependant Code")
