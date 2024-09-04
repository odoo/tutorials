from odoo import models, fields


class DentalPatients(models.Model):

    _name = "dental.patient"
    _description = "Dental patient"

    name = fields.Char(string='Name', required=True)
    state = fields.Selection(string='Status',
                             selection=[
                                 ('new', 'New'),
                                 ('to_do_today', 'To do today'),
                                 ('done', 'Done'),
                                 ('to_invoice', 'To Invoice')
                             ], default='new'
                             )
    gp_id = fields.Many2one('res.partner', string="GP's Name")
    chronic_conditions = fields.Many2many(
        'dental.chronic.condition', string='Chronic Conditions')
    allergies = fields.Many2many('dental.allergy', string='Allergies')
    substance_abuse = fields.Many2many(
        'dental.habit', string='Habits/Substance Abuse')
    hospitalized_this_year = fields.Text(string='Hospitalized this Year')
    medication = fields.Many2many('dental.medication', string='Medication')
    gender = fields.Selection(string='Gender',
                              selection=[
                                  ('male', 'Male'),
                                  ('female', 'Female'),
                                  ('neither', 'Neither'),
                                  ('to_invoice', 'To Invoice')
                              ], default='new'
                              )
    under_specialist_care = fields.Text(string='Under Specialist Care')
    psychiatric_history = fields.Text(string='Psychiatric History')
    pregnant = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Are you pregnant?')
    nursing = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Are you nursing?')
    hormone_treatment = fields.Selection([
        ('hrt', 'Hormone Replacement Treatment'),
        ('birth_control', 'Birth Control'),
        ('neither', 'Neither')
    ], string='Hormone Treatment')
