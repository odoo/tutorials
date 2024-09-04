from odoo import  fields, models


class habitModel(models.Model):
    _name = "symptoms.habits"
    _description = "Habits"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char() 
    sequence = fields.Integer("Sequence")