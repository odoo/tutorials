from odoo import fields, models


class EstateCity(models.Model):
    _inherited = "res.city"
    _name = "estate.city"

    estate_ids = fields.One2many("estate.estate")