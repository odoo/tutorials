from odoo import models, fields


class DentalMedicalAids(models.Model):
    _name = 'dental.medical.aids'
    _description = 'Medical Aids'

    name = fields.Char('Name', required=True)
    contact = fields.Integer('Contact')
    phone = fields.Char('Phone')
    email = fields.Text('Email')
    company_id = fields.Many2one('res.company')
    image = fields.Image('Image')
