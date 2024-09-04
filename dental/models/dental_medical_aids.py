from odoo import fields, models


class MedicalAids(models.Model):

    _name = "dental.medical.aid"
    _description = "Medical Aid Records"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Name")
    contact = fields.Char("Contact")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    company = fields.Char("Company")
    notes = fields.Char("Notes")
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("progress", "In Progress"),
            ("done", "Done"),
        ],
    )
