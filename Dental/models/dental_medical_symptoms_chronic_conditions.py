from odoo import fields, models


class ChronicConditions(models.Model):
    _name = 'dental.chronic.conditions'
    _description = 'Chronic Conditions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(string="Name")
