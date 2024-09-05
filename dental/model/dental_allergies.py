from odoo import fields, models


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Medical symptom(Allergies)"
    _order = "sequence, id desc"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
