from odoo import fields, models

class RecurringPlan(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property"

    name = fields.Char(required=True)