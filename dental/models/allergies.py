from odoo import fields, models


class AllergiesModel(models.Model):
    _name = "symptoms.allergies"
    _description = "Medical Aids"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    sequence = fields.Integer("Sequence")
