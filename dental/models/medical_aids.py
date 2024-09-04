from odoo import fields, models


class DentalMedicalAids(models.Model):
    _name = "medical.aids"
    _description = "This Model is for Medical Aids"

    name = fields.Char()
    contact = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    comapny_id = fields.Char()
    description = fields.Char()
    patient_ids = fields.One2many("dental.patient", "medicalaid_id")
    
