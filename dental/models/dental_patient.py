from odoo import  fields, models


class PatientModel(models.Model):
    _name = "dental.patients"
    _description = "Dental Patients"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("to do today", "To Do Today"),
            ("done", "Done"),
            ("to invoice", "To Invoice"),
        ],
        tracking=True,
        default="new",
    )
    sequence = fields.Integer("Sequence")
    chronic_ids = fields.Many2many("chronic.condition", string="Chronic Condition")
    aleergies_ids = fields.Many2many("symptoms.allergies", string="Allergies")
    habits_ids = fields.Many2many("symptoms.habits", string="Habits")
    medication = fields.Many2many("medication", string="Medication")
    hospitalised_this_year=fields.Text()
    under_special_care=fields.Text()
    psychiatric_history=fields.Text()
    are_you_pregnant = fields.Boolean(string="Are You Pregnant")
    are_you_pregnant = fields.Boolean(string="Are You Pregnant")
    are_you_nursing = fields.Boolean(string="Are You Nursing")
    are_you_on = fields.Selection(
        selection=[
            ("hormon replacement treatment", "Hormon Replacement Treatment"),
            ("birth control", "Birth Control"),
            ("neither", "Neither"),
        ],
    )
    
    