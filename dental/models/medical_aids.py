from odoo import models, fields


class MedicalAids(models.Model):
    _name = "medical.aids"
    _description = "Medical Insurance Info"

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([('new', 'New'), ('inprogress', 'In Progress'), ('done', 'Done')], default='new')
    contact = fields.Many2one('res.partner', string='Contact', required=True)
    phone = fields.Char(related='contact.phone', string='Phone', required=True)
    email = fields.Char(related='contact.email', string='Email', required=True)
    note = fields.Text(string='Notes')
    company = fields.Many2one('res.company', string='Company', required=True)
    image = fields.Binary(string='Image')
