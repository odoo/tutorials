from odoo import fields, models


class RecurringPlan(models.Model):
    _name = "estate_property"
    _description = "estate Recurring plans"
    _order = "sequence"

    Title = fields.Char('Plan Name', required=True, translate=True)

