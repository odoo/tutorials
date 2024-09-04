from odoo import fields, models


class DentalPatients(models.Model):
    _name = "dental.patients"
    _description = "Table contains dental patients details."

    name = fields.Char()
    state = fields.Selection(
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("to do today", "To do today"),
            ("done", "Done"),
            ("to invoice", "To invoice"),
        ],
        tracking=True,
    )
    chronic_condition_ids = fields.Many2many('dental.chronic.conditions')
    hospitalised = fields.Text(string="Hospitalised This Year")
    medication_ids = fields.Many2many('dental.medication')
    allergies_ids = fields.Many2many('dental.allergies')
    habits_ids = fields.Many2many('dental.habits')
    special_care = fields.Text(string="Under Specialist Care")
    psychiatric_history = fields.Text(string="Psychiatric History")
    pregnant = fields.Boolean(string="Are you pregnant?")
    nursing = fields.Boolean(string="Are you nursing?")
    hrt = fields.Selection(string="Are you on...",  selection=[
            ("hrt", "Hormone Replacement Treatment"),
            ("birth control", "Birth Control"),
            ("neither", "Neither"),])
    notes = fields.Text()