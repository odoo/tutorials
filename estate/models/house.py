from odoo import fields, models


class Houses(models.Model):
    _name = "estate.house"
    _description = "House"

    address = fields.Char(string="House Address", required=True)
    house_url = fields.Image(string="House Image")
