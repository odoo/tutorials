from odoo import fields, models


class DentalChronicCondition(models.Model):
    _name = "chronic.condition"
    _description = "This Model is for Medical Aids"

    name = fields.Char(required=True)

