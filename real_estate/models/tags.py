from odoo import fields, models


class Tags(models.Model):
    _name = "estate.tags"
    _description = "Tags for Estate"

    name = fields.Char("Tag", required="True")
