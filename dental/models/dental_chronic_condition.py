from odoo import fields, models


class ChronicCondition(models.Model):
    _name = "dental.chronic.condition"
    _description = "Chronic Dental Conditions"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'sequence ASC'
    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer()
 