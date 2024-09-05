from odoo import models, fields


class DentalMedication(models.Model):

    _name = "dental.medication"
    _description = "Dental Medication"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
