from odoo import fields, models


class DentalMedication(models.Model):
    _name = "dental.medication"
    _description = "Table contains patient medication details."

    name = fields.Char()
    sequence = fields.Integer("Sequence")
