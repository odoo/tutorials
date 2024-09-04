from odoo import models, fields


class DentalMedicalSymptoms(models.Model):

    _name = "dental.medical.symptoms"
    _description = "Dental medical symptoms"

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one("dental.medical.symptoms")
    sequence = fields.Integer('Sequence', default=1)


class DentalAllergy(models.Model):

    _name = "dental.allergy"
    _description = "Dental allergy"
    _inherits = {'dental.medical.symptoms': 'symptoms_id'}

    symptoms_id = fields.Many2one('dental.medical.symptoms')


class DentalChronicCondition(models.Model):

    _name = "dental.chronic.condition"
    _description = "Dental chronic condition"
    _inherits = {'dental.medical.symptoms': 'symptoms_id'}

    symptoms_id = fields.Many2one('dental.medical.symptoms')


class DentalMedicalAids(models.Model):

    _name = "dental.habit"
    _description = "Dental habit"
    _inherits = {'dental.medical.symptoms': 'symptoms_id'}

    symptoms_id = fields.Many2one('dental.medical.symptoms')
