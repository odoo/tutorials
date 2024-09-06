from odoo import fields, models


class DentalMedicalAids(models.Model):
    _name = "medical.aids"
    _description = "This Model is for Medical Aids"

    name = fields.Char()
    contact = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    comapny_id = fields.Char()
    description = fields.Text()
    state = fields.Selection(
        default="new",
        selection=[("new", "New"), ("inprogress", "In Progress"), ("done", "Done")],
    )
    sequence = fields.Integer(
        "Sequence",
        default=1,
    )
