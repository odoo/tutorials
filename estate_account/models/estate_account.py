from odoo import models, fields


class EstateAccount(models.Model):
    _name = "estate.account"
    _description = "Account of real estate"
    _order = "name asc"

    name = fields.Char(required=True)
