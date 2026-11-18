from odoo import fields, models


class RecurringPlan(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"

    name = fields.Char(required=True)
