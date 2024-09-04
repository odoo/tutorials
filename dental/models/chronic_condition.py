from odoo import  fields, models


class ChronicModel(models.Model):
    _name = "chronic.condition"
    _description = "Medical Aids"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char() 
    sequence = fields.Integer("Sequence")