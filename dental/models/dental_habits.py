from odoo import fields, models


class HabitsAbuse(models.Model):
    _name = "dental.habits.abuse"
    _description = "Habits and Abuse Records"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence DESC'
    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer()