from odoo import fields, models


class DentalMedicalAids(models.Model):
    _name = "dental.medical.aids"
    _description = "Table contains patient medical aids details."

    name = fields.Char()
    contact = fields.Char()
    email = fields.Char()
    phone = fields.Integer()
    company = fields.Char()
    notes = fields.Text()
    status = fields.Selection(
        copy=False, default="new", selection=[("new", "New"), ("in progress", "In Progress"), ("done", "Done")]
    )
