from odoo import models, fields


class DentalHabits(models.Model):
    _name = 'dental.habits'
    _description = 'Dental habits and substance abuse list'
    _order = 'name'

    name = fields.Char(string="Habits/Substance Abuse", required=True)
    sequence = fields.Integer(string='Sequence', default=10)
