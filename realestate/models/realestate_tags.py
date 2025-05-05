from odoo import fields, models


class Tags(models.Model):
    _name = "realestate_tags"
    _order = "name"
    _description = "Tags"
    name = fields.Char(required=True)
    color = fields.Integer(string="Color")  # <-- add this
