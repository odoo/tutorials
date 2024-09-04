from odoo import api, models, fields


class DentalMedication(models.Model):

    _name = "dental.medication"
    _description = "Dental Medication"

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence')
