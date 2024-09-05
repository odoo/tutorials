from odoo import fields, models


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Allergies Records"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence ASC'
    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer()
 