from odoo import fields, models


class EstateAccount(models.Model):
    _name = "estate.account"
    _description = "EstateAccount"
    name = fields.Char(required=True)
