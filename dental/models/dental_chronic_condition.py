from odoo import fields, models


class ChronicCondition(models.Model):
    _name = "dental.chronic.condition"
    _description = "Chronic Dental Conditions"

    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
