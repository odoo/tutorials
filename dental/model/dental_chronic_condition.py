from odoo import fields, models


class ChronicCondition(models.Model):
    _name = "dental.chronic.condition"
    _description = "Medical symptom(Chronic condition)"
    _order = "sequence, id desc"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
