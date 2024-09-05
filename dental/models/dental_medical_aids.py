from odoo import models, fields


class DentalMedicalAids(models.Model):

    _name = "dental.medical.aids"
    _description = "Medical Aids"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    contact_id = fields.Many2one('res.partner', string='Contact')
    phone_number = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    company_id = fields.Many2one('res.company', string='Company')
    notes = fields.Text(string='Notes')
    image = fields.Image("Image")

    state = fields.Selection(string='Status', default='new',
                             selection=[('new', 'New'), ('in progress', 'In Progress'), ('done', 'Done')])
