from odoo import models, fields

class Habits(models.Model):
    _name = 'dental.habit.substance.abuse'
    _description = 'Habits'

    name = fields.Char(string="Name")
