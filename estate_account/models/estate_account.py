from odoo import fields, models


class EstateAccount(models.Model):
    _name = "estate.account"
    name = fields.Char(required=True)
