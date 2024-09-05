from odoo import models, fields


class DentalMedicalSymptoms(models.Model):

    _name = "dental.medical.symptoms"
    _description = "Dental Medical Symptoms"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
