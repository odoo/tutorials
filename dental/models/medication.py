from odoo import models, fields


class Medication(models.Model):
    _name = "dental.medication"
    _description = "Medicinal Info"
    _order = "sequence, name"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer()
