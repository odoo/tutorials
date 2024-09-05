from odoo import models, fields


class DentalChronicConditions(models.Model):

    _name = "dental.chronic.conditions"
    _description = "Dental Chronic Conditions"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence')
    parent_id = fields.Many2one('dental.chronic.conditions')
