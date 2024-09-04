from odoo import fields, models


class medication(models.Model):
    _name = "dental.medication"
    _description = "Medication"
    
    name = fields.Char(required = True)
    patient_ids = fields.One2many("dental.patient", "medical_aids_ids")