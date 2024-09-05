from odoo import fields, models


class MedicationModel(models.Model):
    _name = "medication"
    _description = "Medication"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Medication")
    sequence = fields.Integer("Sequence")
