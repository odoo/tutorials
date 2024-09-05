from odoo import models, fields


class DentalChronicCondition(models.Model):

    _name = "dental.chronic.condition"
    _description = "Dental chronic condition"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one("dental.chronic.condition")
    sequence = fields.Integer('Sequence', default=1)


class DentalAllergy(models.Model):

    _name = "dental.allergy"
    _description = "Dental allergy"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one("dental.allergy")
    sequence = fields.Integer('Sequence', default=1)


class DentalMedicalAids(models.Model):

    _name = "dental.habit"
    _description = "Dental habit"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one("dental.habit")
    sequence = fields.Integer('Sequence', default=1)
