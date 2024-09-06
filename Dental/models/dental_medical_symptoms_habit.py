from odoo import models, fields


class Habits(models.Model):
    _name = 'dental.habit.substance.abuse'
    _description = 'Habits'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(string="Name")
