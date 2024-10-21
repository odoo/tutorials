from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Estate Name", required=True, translate=True)
    price = fields.Integer("Estate Price", default=0)
