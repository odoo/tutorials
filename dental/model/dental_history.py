from odoo import fields, models


class History(models.Model):
    _name = "dental.history"
    _description = "History of patients"
    date = fields.Date()
    description = fields.Char()
    tags = fields.Char()
    patient = fields.Many2one("dental.patient")