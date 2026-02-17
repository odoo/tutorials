from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags module for Odoo 19 tutorials Hello World"

    name = fields.Char(required=True, string="Tag Name")
