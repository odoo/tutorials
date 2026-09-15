from odoo import models, fields


class Property(models.Model):
    _name = "property"
    _description = "Estate Property"

    name = fields.Char()
