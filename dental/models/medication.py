from odoo import fields, models


class DentalMedications(models.Model):
    _name = "medication"
    _description = "This Model is for Medication"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence",
        default=1,
    )
