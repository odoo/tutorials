from odoo import fields, models


class medication(models.Model):
    _name = "dental.medication"
    _description = "Medication"
    _order = "sequence, id desc"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
