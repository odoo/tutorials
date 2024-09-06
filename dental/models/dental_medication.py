from odoo import models, fields


class DentalMedication(models.Model):
    _name = "dental.medication"
    _description = "Medications"
    _order = "name"

    name = fields.Char(string="Medication", required=True)
