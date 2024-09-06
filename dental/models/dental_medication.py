from odoo import fields, models


class Medication(models.Model):
    _name = "dental.medication"
    _description = "Medication"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence DESC'
    name = fields.Char("Name", required=True)
    patients_id = fields.Many2one("dental.patients", string="Patient")
    sequence = fields.Integer()
