from odoo import fields, models


class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Tag Name", required=True)
