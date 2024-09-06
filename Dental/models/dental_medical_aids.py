from odoo import models, fields


class DentalMedicalAids(models.Model):
    _name = 'dental.medical.aids'
    _description = 'Medical Aids'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    contact = fields.Many2one('res.partner', 'Contact')
    phone = fields.Char('Phone')
    email = fields.Text('Email')
    company_id = fields.Many2one('res.company')
    image = fields.Image('Image')
