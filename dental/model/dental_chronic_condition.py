from odoo import fields, models


class ChronicCondition(models.Model):
    _name = "dental.chronic.condition"
    _description = "Medical symptom(Chronic condition)"
    
    name = fields.Char(required = True)
    