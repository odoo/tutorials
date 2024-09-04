from odoo import models, fields


class Medication(models.Model):
    _name = "dental.medication"
    _description = "Medicinal Info"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
