from odoo import fields, models


class DentalHabits(models.Model):
    _name = "habits"
    _description = "This Model is for Medical habits"

    name = fields.Char(required=True)

