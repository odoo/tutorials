from odoo import models, fields


class DentalMedication(models.Model):
    _name = 'dental.medication'
    _description = 'Dental Medication'
    _order = 'sequence, name'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence')
