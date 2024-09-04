from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta


class DentalPatients(models.Model):
    _name = "dental.patient"
    _description = "patients"

    name = fields.Char(string='Name', required=True)
    stage = fields.Selection(
        string='Stage',
        selection=[('new', 'New'), ('to do today', 'To Do Today'), ('done', 'Done'), ('to invoice', 'To Invoice')],
        help='stage of the appointment',
        required=True,
        default='new')
    doctor_id = fields.Many2one(
        'res.partner',
        string="GP's Name",
        copy=False,
        help="The Genereal practioner for this patient")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        copy=False
    )
    phone_number = fields.Char(string="GP's Phone", related="doctor_id.phone")
    chronic_conditions_ids = fields.Many2many('chronic.conditions', string="Chronic Condtions")
    allergies_ids = fields.Many2many('dental.allergies', string="Allergies")
    habits_substance_ids = fields.Many2many('habits.substance', string="Habits and substance abuse")
    medication_ids = fields.Many2many('dental.medication', string="Medication")
    hospitialized = fields.Char(string="Hospitalized this year")
    specialized_care = fields.Char(string="Under Specialist Care")
    psychiatric_history = fields.Char(string="Psychiatric history")
    gender = fields.Selection(
        string="Gender",
        selection=[('female', 'Female'), ('male', 'Male'), ('neither', 'Neither')],
        required=True,
        default='neither')
    pregnant = fields.Boolean(string="Are you pregnant?", required=True, default=False)
    nursing = fields.Boolean(string="Are you nursing?", required=True, default=False)
    hormone = fields.Selection(
        string="Are you on hormone therapy?",
        selection=[('hrt', 'Hormone Replacement Treatment'), ('birth control', 'Birth Conrol'), ('neither', 'Neither')],
        required=True,
        default='neither')
    occupation = fields.Char(string="Occupation")
    identity_num = fields.Char(string="Identity number")
    birthdate = fields.Date(string="Date of birth", required=True)
    maritial_status = fields.Selection(
        string="Maritial Status",
        selection=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')],
        required=True,
        default='single')
