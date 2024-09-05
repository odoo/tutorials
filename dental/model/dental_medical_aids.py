from odoo import fields, models


class DentalMedicalAids(models.Model):
    _name = "dental.medical.aids"
    _description = "dental medical aids"
    _order = "sequence, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
    phone_number = fields.Char()
    email = fields.Char()
    notes = fields.Char()
    patient_ids = fields.One2many("dental.patient", "medical_aids_ids")
    company_id = fields.Many2one("res.company")
    image = fields.Image()

    state = fields.Selection(
        default="new",
        selection=[
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        tracking=True,
    )
