from odoo import fields, models


class Tags(models.Model):
    _name = "tags"

    name = fields.Char(required=True)
