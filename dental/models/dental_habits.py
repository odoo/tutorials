from odoo import fields, models


class DentalHabits(models.Model):
    _name = "dental.habits"
    _description = "Table contains patient habit details."

    name = fields.Char()
    sequence = fields.Integer("Sequence")