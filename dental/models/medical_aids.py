from odoo import models, fields


class MedicalAids(models.Model):
    _name = "medical.aids"
    _description = "Medical Insurance Info"

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        copy=False,
        help='Insured Patient')
    phone_number = fields.Char(string='Phone Number')
    email_address = fields.Char(string='Email ID')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company.id
    )
    note = fields.Text(string="")
    image = fields.Image(string="")
