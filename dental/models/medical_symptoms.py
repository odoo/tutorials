from odoo import models, fields


class ChronicConditions(models.Model):
    _name = "chronic.conditions"
    _description = "Chronic medical symptoms"
    _order = "sequence, name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
    sequence = fields.Integer()
    parent_id = fields.Many2one('chronic.conditions', ondelete='cascade', index=True)


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Allergies"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
    sequence = fields.Integer()
    parent_id = fields.Many2one('dental.allergies', ondelete='cascade', index=True)


class HabitsSubstance(models.Model):
    _name = "habits.substance"
    _description = "Habits and substance abuse info"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
    sequence = fields.Integer()
    parent_id = fields.Many2one('habits.substance', ondelete='cascade', index=True)
