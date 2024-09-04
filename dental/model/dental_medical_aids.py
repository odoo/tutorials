from odoo import fields, models


class DentalMedicalAids(models.Model):
    _name = "dental.medical.aids"
    _description = "dental medical aids"
    
    name = fields.Char(required=True)
    phone_number = fields.Integer()
    email = fields.Char()
    notes = fields.Char()