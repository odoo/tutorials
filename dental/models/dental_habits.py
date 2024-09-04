from odoo import fields, models


class HabitsAbuse(models.Model):
    _name = "dental.habits.abuse"
    _description = "Habits and Abuse Records"
    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
   