from odoo import fields, models


class Tags(models.Model):
    _name = "tags"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer(string="Color")  # <-- add this
