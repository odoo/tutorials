from odoo import fields, models


class HabitsAbuse(models.Model):
    _name = "dental.habits.abuse"
    _description = "Medical symptom(Habits/abuses)"
    
    name = fields.Char(required = True)