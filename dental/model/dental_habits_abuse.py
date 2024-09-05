from odoo import fields, models


class HabitsAbuse(models.Model):
    _name = "dental.habits.abuse"
    _description = "Medical symptom(Habits/abuses)"
    _order = "sequence, id desc"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")
