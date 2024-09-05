from odoo import fields, models


class MedicalAids(models.Model):

    _name = "dental.medical.aid"
    _description = "Medical Aid Records"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence DESC'
    name = fields.Char("Name")
    image = fields.Image("Medical Aid")
    contact = fields.Char("Contact")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    company_id = fields.Many2one("res.company")
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
    sequence = fields.Integer()