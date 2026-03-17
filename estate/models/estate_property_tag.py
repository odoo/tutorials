from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate system - Property Tag"

    name = fields.Char(string="Tag Name", required=True)
