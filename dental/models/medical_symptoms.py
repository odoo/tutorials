from odoo import models, fields


class ChronicConditions(models.Model):
    _name = "chronic.conditions"
    _description = "Chronic medical conditions"
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')
    parent_id = fields.Many2one('chronic.conditions', string='Parent Condition', ondelete='cascade', index=True)


class Allergies(models.Model):
    _name = "dental.allergies"
    _description = "Allergies"

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one('chronic.conditions', string='Parent Condition', ondelete='cascade', index=True)


class HabitsSubstance(models.Model):
    _name = "habits.substance"
    _description = "Habits and substance abuse information"

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one('chronic.conditions', string='Parent Condition', ondelete='cascade', index=True)
