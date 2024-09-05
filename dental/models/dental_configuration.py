from odoo import models, fields


class DentalConfiguration(models.Model):

    _name = "dental.configuration"
    _description = "Dental Configuration"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
