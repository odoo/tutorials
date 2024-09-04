from odoo import fields, models


class DentalAllergies(models.Model):
    _name = "dental.allergies"
    _description = "Table contains patient allergies details."

    name = fields.Char()
    sequence = fields.Integer("Sequence")