from odoo import fields, models
from datetime import date, timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.tags"
    _description = "common characteristics of the properties"

    name = fields.Char('Property Tag Name',required=True)
    properties = fields.Many2many("estate.property","tag_ids",string="properties")
    color = fields.Integer(string="Color") 
    _order ="name"


    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'There is already a tag with this name'),
    ]
