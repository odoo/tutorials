from odoo import models, fields


class DentalHabits(models.Model):

    _name = "dental.habits"
    _description = "Dental Habits"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
