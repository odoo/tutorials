from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.tag"
    _description = "Real_Estate property model"

    name = fields.Char('Name', required=True)
