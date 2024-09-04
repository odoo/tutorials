from odoo import api, models, fields


class DentalHabits(models.Model):

    _name = "dental.habits"
    _description = "Dental Habits"

    name = fields.Char(string='Name')
