from odoo import models, fields


class DentalAllergies(models.Model):

    _name = "dental.allergies"
    _description = "Dental Allergies"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
