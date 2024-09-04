from odoo import api, models, fields


class DentalChronicConditions(models.Model):

    _name = "dental.chronic.conditions"
    _description = "Dental Chronic Conditions"

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence')
    parent_id = fields.Many2one('dental.chronic.conditions')
