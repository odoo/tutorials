from odoo import api, models, fields


class DentalMedicalSymptoms(models.Model):

    _name = "dental.medical.symptoms"
    _description = "Dental Medical Symptoms"

    name = fields.Char(string='Name')
