from importlib.metadata import requires

from odoo import fields, models


class Estate(models.Model):
    _name = "estate.estate"
    _description = "This is the estate model."

    status_id = fields.Many2one("estate.status")
    price = fields.Float()
    bed = fields.Integer()
    bath = fields.Integer()
    street = fields.Char()
    city = fields.Many2one("res.city")
    house_size = fields.Float()


class Status(models.Model):
    _name = "estate.status"
    _description = "This is the description."

    name = fields.Char(required=True)