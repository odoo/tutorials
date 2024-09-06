from odoo import models, fields


class DentalChronicDiseases(models.Model):
    _name = "dental.chronic.diseases"
    _description = "Dental chronic diseases list"
    _order = "name"

    name = fields.Char(string="Chronic Condition", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
