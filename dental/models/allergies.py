from odoo import fields, models


class DentalAllegies(models.Model):
    _name = "allergies"
    _description = "This Model is for Medical Allergies"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence",
        default=1,
    )
