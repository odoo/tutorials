from odoo import fields, models
from datetime import date, timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.tags"
    _description = "common characteristics of the properties"

    name = fields.Char('Property Tag Name',required=True)
    properties = fields.Many2many("estate.property","tag_ids",string="properties")
