from odoo import models, fields


class MedicalSymptoms(models.Model):
    _name = "medical.symptoms"
    _description = "All the underlying conditions"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    parent_id = fields.Many2one('medical.symptoms')

class ChronicConditions(models.Model):
    _name = "chronic.conditions"
    _description = "Chronic medical symptoms"
    _inherits = {'medical.symptoms':'medical_symptoms_id'}

    medical_symptoms_id = fields.Many2one('medical.symptoms')
class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Allergies"
    _inherits = {'medical.symptoms':'medical_symptoms_id'}

    medical_symptoms_id = fields.Many2one('medical.symptoms')

class HabitsSubstance(models.Model):
    _name = "habits.substance"
    _description = "Habits and substance abuse info"
    _inherits = {'medical.symptoms':'medical_symptoms_id'}

    medical_symptoms_id = fields.Many2one('medical.symptoms')
