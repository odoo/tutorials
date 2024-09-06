from odoo import models, fields


class Allergies(models.Model):
    _name = 'dental.allergies'
    _description = 'Allergies'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(string="Name")
